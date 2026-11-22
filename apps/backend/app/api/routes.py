from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
import json
import logging

from app.database.connection import get_db
from app.database.models import DocumentModel
from app.documents.manager import document_manager
from app.orchestration.engine import orchestrator
from app.routing.strategy import AnswerMode
from app.llm.factory import llm_factory
from app.monitoring.metrics import metrics_collector
from app.transcripts.manager import transcript_manager

logger = logging.getLogger("ai_voice_copilot.api.routes")
router = APIRouter()

class GenerateAnswerRequest(BaseModel):
    question: str
    mode: str = "fast"

class GenerateAnswerResponse(BaseModel):
    id: str
    question: str
    answer: str
    mode: str
    provider: str
    model: str
    latencyMs: float
    sources: List[str]
    createdAt: str

@router.post("/generate-answer", response_model=GenerateAnswerResponse)
async def generate_answer(req: GenerateAnswerRequest):
    """
    Primary endpoint triggered by the desktop 'Generate Answer' button.
    Executes mandatory RAG, routes to fastest available LLM, and logs performance.
    """
    try:
        mode_enum = AnswerMode(req.mode.lower())
    except ValueError:
        mode_enum = AnswerMode.FAST

    result = await orchestrator.process_question(question=req.question, mode=mode_enum)
    return result

@router.post("/generate-answer-stream")
async def generate_answer_stream(req: GenerateAnswerRequest):
    """
    Server-Sent Events (SSE) streaming endpoint for real-time token delivery.
    Delivers sub-second first-token response to the desktop frontend.
    """
    try:
        mode_enum = AnswerMode(req.mode.lower())
    except ValueError:
        mode_enum = AnswerMode.FAST

    async def event_generator():
        async for event in orchestrator.process_question_stream(question=req.question, mode=mode_enum):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/documents")
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentModel).order_by(DocumentModel.upload_timestamp.desc()))
    docs = result.scalars().all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "format": d.format,
            "fileSize": d.file_size,
            "uploadedAt": d.upload_timestamp.isoformat(),
            "status": d.processing_status,
            "chunkCount": d.chunk_count,
            "errorMessage": d.error_message,
        }
        for d in docs
    ]

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 50MB limit")

    doc_record = await document_manager.ingest_document(
        filename=file.filename,
        content=content,
        db=db,
    )
    return {
        "id": doc_record.id,
        "filename": doc_record.filename,
        "format": doc_record.format,
        "fileSize": doc_record.file_size,
        "uploadedAt": doc_record.upload_timestamp.isoformat(),
        "status": doc_record.processing_status,
        "chunkCount": doc_record.chunk_count,
    }

@router.post("/documents/reindex")
async def reindex_documents(db: AsyncSession = Depends(get_db)):
    """
    Indexes all files currently in storage/documents/originals (such as candidate transcripts).
    """
    count = await document_manager.reindex_all_existing_documents(db)
    return {"status": "reindexed", "filesProcessed": count}

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    await document_manager.delete_document(doc_id=doc_id, db=db)
    return {"success": True, "id": doc_id}

@router.get("/documents/{doc_id}/preview")
async def preview_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentModel).where(DocumentModel.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        with open(doc.extracted_path, "r", encoding="utf-8") as f:
            content = f.read(5000)
        return {"id": doc.id, "filename": doc.filename, "preview": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read preview: {e}")

@router.get("/config/providers")
async def get_providers():
    return llm_factory.list_providers()

@router.get("/metrics")
async def get_metrics():
    return metrics_collector.get_summary()

@router.get("/transcripts/recent")
async def get_recent_transcripts():
    return transcript_manager.get_recent_context(count=15)

@router.get("/status")
async def get_system_status():
    return {
        "audio_engine": "system_audio_loopback",
        "stt": "whisper_local",
        "database": "sqlite_async",
        "vector_store": "chromadb_local",
        "persona": "Santosh Neelappagol (~4y Python Full Stack & AI)",
    }
