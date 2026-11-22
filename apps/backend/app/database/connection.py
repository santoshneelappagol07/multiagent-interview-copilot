from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings
from app.database.models import Base
import logging
from pathlib import Path

logger = logging.getLogger("ai_voice_copilot.database")

# Ensure database directory exists
db_url = settings.database_url
if "sqlite" in db_url:
    raw_path = db_url.split(":///")[-1]
    db_file_path = Path(raw_path)
    db_file_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_async_engine(settings.database_url, echo=False)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    logger.info("Initializing SQLite database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database schema initialized.")

async def get_db():
    async with async_session_factory() as session:
        yield session
