from typing import List, Dict, Any
import re

class TextChunker:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if not text.strip():
            return []

        # Split into paragraphs and sentences
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = []
        current_len = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            words = para.split()
            if current_len + len(words) <= self.chunk_size:
                current_chunk.append(para)
                current_len += len(words)
            else:
                if current_chunk:
                    chunk_text = "\n\n".join(current_chunk)
                    chunks.append({
                        "text": chunk_text,
                        "metadata": {**(metadata or {}), "chunk_index": len(chunks)},
                    })
                current_chunk = [para]
                current_len = len(words)

        if current_chunk:
            chunks.append({
                "text": "\n\n".join(current_chunk),
                "metadata": {**(metadata or {}), "chunk_index": len(chunks)},
            })

        return chunks

text_chunker = TextChunker()
