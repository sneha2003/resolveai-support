"""Embed all chunks and upsert them with metadata into persistent Qdrant."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"backend"))
from app.config import get_settings
from app.repository import KnowledgeRepository

def run():
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance,PointStruct,VectorParams
    from sentence_transformers import SentenceTransformer
    settings=get_settings(); repo=KnowledgeRepository(); model=SentenceTransformer(settings.embedding_model); client=QdrantClient(url=settings.qdrant_url)
    texts=[f"{c.title}\n{c.section_title}\n{c.text}" for c in repo.chunks]; vectors=model.encode(texts,normalize_embeddings=True,show_progress_bar=True)
    collection="resolveai_chunks"
    if client.collection_exists(collection): client.delete_collection(collection)
    client.create_collection(collection_name=collection,vectors_config=VectorParams(size=len(vectors[0]),distance=Distance.COSINE))
    batch=[]
    for index,(chunk,vector) in enumerate(zip(repo.chunks,vectors)):
        payload=chunk.model_dump(); batch.append(PointStruct(id=index,vector=vector.tolist(),payload=payload))
        if len(batch)==128: client.upsert(collection_name=collection,points=batch); batch=[]
    if batch: client.upsert(collection_name=collection,points=batch)
    print(f"Indexed {len(repo.chunks)} chunks from {len(repo.documents)} documents into {collection}.")
if __name__=="__main__": run()
