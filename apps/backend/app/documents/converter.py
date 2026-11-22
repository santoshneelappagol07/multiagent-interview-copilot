from pathlib import Path
import fitz  # PyMuPDF
from docx import Document as DocxDocument
import logging

logger = logging.getLogger("ai_voice_copilot.documents.converter")

class DocumentConverter:
    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        text_parts = []
        with fitz.open(str(file_path)) as doc:
            for page in doc:
                text_parts.append(page.get_text())
        return "\n\n".join(text_parts)

    @staticmethod
    def extract_text_from_docx(file_path: Path) -> str:
        doc = DocxDocument(str(file_path))
        return "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    @staticmethod
    def extract_text_from_txt(file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @classmethod
    def convert_to_plaintext(cls, file_path: Path, format_ext: str) -> str:
        ext = format_ext.lower().lstrip(".")
        if ext == "pdf":
            return cls.extract_text_from_pdf(file_path)
        elif ext in ["docx", "doc"]:
            return cls.extract_text_from_docx(file_path)
        elif ext == "txt":
            return cls.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
