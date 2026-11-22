from pathlib import Path
import shutil
import uuid
from typing import List, Dict, Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.models import DocumentModel
from app.documents.converter import DocumentConverter
from app.documents.processor import TextNormalizer
from app.rag.chunker import text_chunker
from app.rag.embeddings import embedding_service
from app.embeddings.store import vector_store
import logging

logger = logging.getLogger("ai_voice_copilot.documents.manager")

class DocumentManager:
    def __init__(
        self,
        originals_dir: str = None,
        extracted_dir: str = None
    ):
        orig_path = originals_dir or settings.documents_original_path
        extr_path = extracted_dir or settings.documents_extracted_path
        self.originals_dir = Path(orig_path).resolve()
        self.extracted_dir = Path(extr_path).resolve()
        self.originals_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_dir.mkdir(parents=True, exist_ok=True)

    async def ingest_document(
        self, filename: str, content: bytes, db: AsyncSession
    ) -> DocumentModel:
        doc_id = str(uuid.uuid4())
        ext = filename.split(".")[-1].lower() if "." in filename else "txt"

        original_file = self.originals_dir / f"{doc_id}_{filename}"
        extracted_file = self.extracted_dir / f"{doc_id}.txt"

        # 1. Save original binary
        with open(original_file, "wb") as f:
            f.write(content)

        # 2. Extract plain text and normalize
        raw_text = DocumentConverter.convert_to_plaintext(original_file, ext)
        normalized_text = TextNormalizer.normalize(raw_text)

        # 3. Save extracted plain text locally
        with open(extracted_file, "w", encoding="utf-8") as f:
            f.write(normalized_text)

        # 4. Chunk text
        chunks = text_chunker.chunk(normalized_text, metadata={"doc_id": doc_id, "filename": filename})
        chunk_texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]

        # 5. Generate embeddings and index in ChromaDB
        if chunk_texts:
            embeddings = embedding_service.embed_batch(chunk_texts)
            vector_store.add_chunks(doc_id, chunk_texts, embeddings, metadatas)

        # 6. Save document record in SQLite
        doc_record = DocumentModel(
            id=doc_id,
            filename=filename,
            format=ext,
            file_size=len(content),
            original_path=str(original_file),
            extracted_path=str(extracted_file),
            processing_status="indexed",
            chunk_count=len(chunks),
            embedding_status="ready",
        )
        db.add(doc_record)
        await db.commit()
        await db.refresh(doc_record)

        logger.info(f"Ingested document '{filename}' with {len(chunks)} chunks.")
        return doc_record

    async def ingest_existing_file(self, file_path: Path, db: AsyncSession) -> DocumentModel:
        """Ingests a file that is already present on disk in the originals folder."""
        filename = file_path.name
        # Check if already indexed in database
        result = await db.execute(select(DocumentModel).where(DocumentModel.filename == filename))
        existing = result.scalar_one_or_none()
        if existing:
            return existing

        with open(file_path, "rb") as f:
            content = f.read()

        doc_id = str(uuid.uuid4())
        ext = filename.split(".")[-1].lower() if "." in filename else "txt"
        extracted_file = self.extracted_dir / f"{doc_id}.txt"

        raw_text = DocumentConverter.convert_to_plaintext(file_path, ext)
        normalized_text = TextNormalizer.normalize(raw_text)

        with open(extracted_file, "w", encoding="utf-8") as f:
            f.write(normalized_text)

        chunks = text_chunker.chunk(normalized_text, metadata={"doc_id": doc_id, "filename": filename})
        chunk_texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]

        if chunk_texts:
            embeddings = embedding_service.embed_batch(chunk_texts)
            vector_store.add_chunks(doc_id, chunk_texts, embeddings, metadatas)

        doc_record = DocumentModel(
            id=doc_id,
            filename=filename,
            format=ext,
            file_size=len(content),
            original_path=str(file_path),
            extracted_path=str(extracted_file),
            processing_status="indexed",
            chunk_count=len(chunks),
            embedding_status="ready",
        )
        db.add(doc_record)
        await db.commit()
        await db.refresh(doc_record)
        logger.info(f"Indexed existing knowledge file '{filename}' ({len(chunks)} chunks).")
        return doc_record

    async def reindex_all_existing_documents(self, db: AsyncSession) -> int:
        """Scans the originals directory and indexes all non-indexed files."""
        indexed_count = 0
        for f in self.originals_dir.iterdir():
            if f.is_file() and not f.name.startswith(".") and f.suffix.lower() in [".txt", ".pdf", ".docx", ".doc"]:
                # If file starts with UUID_ (from previous upload), extract original filename
                await self.ingest_existing_file(f, db)
                indexed_count += 1
        return indexed_count

    async def delete_document(self, doc_id: str, db: AsyncSession):
        # Remove from vector store
        vector_store.delete_document(doc_id)

        # Remove files
        for p in self.originals_dir.glob(f"{doc_id}_*"):
            p.unlink(missing_ok=True)
        (self.extracted_dir / f"{doc_id}.txt").unlink(missing_ok=True)

        # Remove from DB
        await db.execute(delete(DocumentModel).where(DocumentModel.id == doc_id))
        await db.commit()
        logger.info(f"Removed document {doc_id} and its vector chunks.")

document_manager = DocumentManager()
