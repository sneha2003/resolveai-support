import json
from pathlib import Path
from app.config import get_settings
from app.ingestion.chunker import chunk_markdown
from app.ingestion.parser import parse_markdown
from app.schemas import Chunk, DocumentDetail, DocumentSummary

class KnowledgeRepository:
    def __init__(self,raw_dir:Path|None=None,include_synthetic:bool|None=None):
        self.raw_dir=raw_dir or get_settings().project_root/"data"/"raw"
        self.include_synthetic=get_settings().include_synthetic_corpus if include_synthetic is None else include_synthetic
        self.documents:dict[str,DocumentDetail]={}; self.chunks:list[Chunk]=[]
        self.load()
    def load(self)->None:
        self.documents={}; self.chunks=[]
        if not self.raw_dir.exists(): return
        paths=self.raw_dir.rglob("*.md") if self.include_synthetic else (
            path for folder in ("external","stackoverflow","uploads") for path in (self.raw_dir/folder).glob("*.md")
        )
        for path in sorted(paths):
            metadata,content=parse_markdown(path); chunks=chunk_markdown(metadata,content)
            doc=DocumentDetail(document_id=str(metadata["document_id"]),title=str(metadata.get("title","")),document_type=str(metadata.get("document_type","product_doc")),service=str(metadata.get("service","platform")),version=str(metadata.get("version","")),updated_at=str(metadata.get("updated_at","")),environment=metadata.get("environment",[]),tags=metadata.get("tags",[]),chunk_count=len(chunks),publisher=str(metadata.get("publisher","")),source_url=str(metadata.get("source_url","")),content=content)
            self.documents[doc.document_id]=doc; self.chunks.extend(chunks)
    def summaries(self)->list[DocumentSummary]:
        return [DocumentSummary(**d.model_dump(exclude={"content"})) for d in self.documents.values()]

repository=KnowledgeRepository()
