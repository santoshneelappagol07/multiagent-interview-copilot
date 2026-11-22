from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import asyncio

from app.config import settings
from app.database.connection import init_db, async_session_factory
from app.documents.manager import document_manager
from app.api.routes import router as api_router
from app.api.websocket import websocket_endpoint, router as ws_router
from app.integrations.grpc_listener import start_grpc_listener

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ai_voice_copilot")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AI Voice Copilot Backend...")
    # Initialize SQLite schema
    await init_db()

    # Index any existing documents in storage/documents/originals (including Santosh's transcripts)
    async with async_session_factory() as session:
        try:
            indexed = await document_manager.reindex_all_existing_documents(session)
            logger.info(f"Auto-indexed {indexed} knowledge base files on startup.")
        except Exception as e:
            logger.warning(f"Initial knowledge base scan: {e}")

    # Start background gRPC listener for Rust Audio STT stream
    grpc_task = asyncio.create_task(start_grpc_listener())
    logger.info("Backend started successfully.")
    yield
    logger.info("Shutting down backend...")
    grpc_task.cancel()

app = FastAPI(
    title="AI Voice Copilot & Interview Assistant Backend",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(ws_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-voice-copilot-backend",
        "audio_mode": "system_audio_loopback",
        "persona": "Santosh Neelappagol (~4y Python Full Stack & AI)",
    }
