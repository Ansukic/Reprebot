import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from app.core.config import get_settings


class VectorStore:
    """Store vectorial plano: matriz numpy + metadatos JSON, persistido en disco."""

    def __init__(self):
        self.lock = threading.Lock()
        self.vectors = np.zeros((0, get_settings().embeddings_dim), dtype=np.float32)
        self.chunks: list[dict] = []
        self.docs: dict[str, dict] = {}
        self.dir = Path(get_settings().data_dir)

    def load(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        vpath = self.dir / "vectors.npy"
        cpath = self.dir / "chunks.json"
        dpath = self.dir / "docs.json"
        if vpath.exists() and cpath.exists():
            self.vectors = np.load(vpath)
            self.chunks = json.loads(cpath.read_text())
            self.docs = (
                {d["id"]: d for d in json.loads(dpath.read_text())}
                if dpath.exists()
                else {}
            )

    def save(self):
        np.save(self.dir / "vectors.npy", self.vectors)
        (self.dir / "chunks.json").write_text(
            json.dumps(self.chunks, ensure_ascii=False)
        )
        (self.dir / "docs.json").write_text(
            json.dumps(list(self.docs.values()), ensure_ascii=False)
        )

    def add(self, doc_name: str, texts: list[str], vectors: np.ndarray) -> dict:
        doc_id = uuid.uuid4().hex
        with self.lock:
            for text in texts:
                self.chunks.append(
                    {
                        "id": uuid.uuid4().hex,
                        "doc_id": doc_id,
                        "doc_name": doc_name,
                        "text": text,
                    }
                )
            self.vectors = np.vstack([self.vectors, vectors])
            self.docs[doc_id] = {
                "id": doc_id,
                "name": doc_name,
                "chunks": len(texts),
                "added_at": datetime.now(timezone.utc).isoformat(),
            }
            self.save()
        return self.docs[doc_id]

    def remove_doc(self, doc_id: str) -> bool:
        with self.lock:
            if doc_id not in self.docs:
                return False
            keep = [i for i, c in enumerate(self.chunks) if c["doc_id"] != doc_id]
            self.chunks = [self.chunks[i] for i in keep]
            if keep:
                self.vectors = self.vectors[keep]
            else:
                self.vectors = np.zeros(
                    (0, get_settings().embeddings_dim), dtype=np.float32
                )
            del self.docs[doc_id]
            self.save()
        return True

    def search(self, vector: np.ndarray, k: int) -> list[dict]:
        if not self.chunks:
            return []
        # vectores normalizados: producto punto = coseno
        scores = self.vectors @ vector
        top = np.argsort(scores)[::-1][:k]
        return [{**self.chunks[i], "score": float(scores[i])} for i in top]

    def list_docs(self) -> list[dict]:
        return list(self.docs.values())

    def stats(self) -> dict:
        return {"documents": len(self.docs), "chunks": len(self.chunks)}


store = VectorStore()
