import math
import re
from collections import Counter
from app.schemas import Chunk, RankedChunk

def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[-_./][a-z0-9]+)*", text.lower())

class BM25Retriever:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = .75):
        self.chunks, self.k1, self.b = chunks, k1, b
        self.docs = [tokenize(f"{c.document_id} {c.title} {c.section_title} {c.text}") for c in chunks]
        self.freqs = [Counter(doc) for doc in self.docs]
        self.avgdl = sum(map(len, self.docs)) / max(1, len(self.docs))
        df = Counter(t for doc in self.docs for t in set(doc))
        self.idf = {t: math.log(1 + (len(self.docs)-n+.5)/(n+.5)) for t,n in df.items()}

    def search(self, query: str, top_k: int = 20, filters: dict | None = None) -> list[RankedChunk]:
        terms, scored = tokenize(query), []
        for chunk, doc, freq in zip(self.chunks, self.docs, self.freqs):
            if filters and any(str(getattr(chunk,k,"")) != str(v) for k,v in filters.items() if v): continue
            score = sum(self.idf.get(t,0)*(freq[t]*(self.k1+1))/(freq[t]+self.k1*(1-self.b+self.b*len(doc)/self.avgdl)) for t in terms if freq[t])
            if score: scored.append((score,chunk))
        scored.sort(key=lambda x:x[0], reverse=True)
        return [RankedChunk(chunk=c,score=s,rank=i,bm25_rank=i) for i,(s,c) in enumerate(scored[:top_k],1)]

class LocalSemanticRetriever:
    SYNONYMS={"checkout":"payment order cart","timeout":"latency unavailable connection","db":"database postgresql","auth":"authentication redis token","lag":"kafka consumer backlog","update":"upgrade release version"}
    def __init__(self,chunks:list[Chunk]):
        self.chunks=chunks; self.docs=[Counter(tokenize(c.text+" "+c.title)) for c in chunks]
        df=Counter(t for d in self.docs for t in d); self.idf={t:math.log((1+len(chunks))/(1+n))+1 for t,n in df.items()}
    def _vec(self,text:str)->Counter:
        expanded=text+" "+" ".join(self.SYNONYMS.get(t,"") for t in tokenize(text)); counts=Counter(tokenize(expanded))
        return Counter({t:n*self.idf.get(t,1) for t,n in counts.items()})
    def _cos(self,a:Counter,b:Counter)->float:
        dot=sum(v*b.get(k,0) for k,v in a.items()); norm=math.sqrt(sum(v*v for v in a.values())*sum(v*v for v in b.values()))
        return dot/norm if norm else 0
    def search(self,query:str,top_k:int=20,filters:dict|None=None)->list[RankedChunk]:
        q,scored=self._vec(query),[]
        for chunk,counts in zip(self.chunks,self.docs):
            if filters and any(str(getattr(chunk,k,"")) != str(v) for k,v in filters.items() if v): continue
            s=self._cos(q,Counter({t:n*self.idf.get(t,1) for t,n in counts.items()}))
            if s: scored.append((s,chunk))
        scored.sort(key=lambda x:x[0],reverse=True)
        return [RankedChunk(chunk=c,score=s,rank=i,dense_rank=i) for i,(s,c) in enumerate(scored[:top_k],1)]

class QdrantVectorRetriever:
    """Production dense retriever; construction fails cleanly when infrastructure is absent."""
    def __init__(self,chunks:list[Chunk],url:str,model_name:str,collection:str="resolveai_chunks"):
        from qdrant_client import QdrantClient
        from sentence_transformers import SentenceTransformer
        self.chunks={c.chunk_id:c for c in chunks}; self.client=QdrantClient(url=url,timeout=2); self.model=SentenceTransformer(model_name); self.collection=collection
        self.client.get_collection(collection)
    def search(self,query:str,top_k:int=20,filters:dict|None=None)->list[RankedChunk]:
        from qdrant_client.models import FieldCondition,Filter,MatchValue
        qfilter=Filter(must=[FieldCondition(key=k,match=MatchValue(value=v)) for k,v in (filters or {}).items()]) if filters else None
        vector=self.model.encode(query,normalize_embeddings=True).tolist()
        hits=self.client.query_points(collection_name=self.collection,query=vector,query_filter=qfilter,limit=top_k,with_payload=True).points
        result=[]
        for rank,hit in enumerate(hits,1):
            chunk=self.chunks.get(str(hit.payload.get("chunk_id")))
            if chunk: result.append(RankedChunk(chunk=chunk,score=float(hit.score),rank=rank,dense_rank=rank))
        return result

def reciprocal_rank_fusion(result_sets:list[list[RankedChunk]],k:int=60)->list[RankedChunk]:
    scores,items={},{}
    for results in result_sets:
        for result in results:
            cid=result.chunk.chunk_id; scores[cid]=scores.get(cid,0)+1/(k+result.rank)
            if cid not in items: items[cid]=result.model_copy(deep=True)
            if result.dense_rank: items[cid].dense_rank=result.dense_rank
            if result.bm25_rank: items[cid].bm25_rank=result.bm25_rank
    ranked=sorted(items.values(),key=lambda x:scores[x.chunk.chunk_id],reverse=True)
    for rank,item in enumerate(ranked,1): item.score=scores[item.chunk.chunk_id]; item.rank=rank; item.rrf_rank=rank
    return ranked

class RerankerService:
    def rerank(self,query:str,candidates:list[RankedChunk],top_k:int=6)->list[RankedChunk]:
        q=set(tokenize(query)); q_codes={term for term in q if re.fullmatch(r"[a-z]+-\d+",term)}
        for c in candidates:
            haystack=c.chunk.text+" "+c.chunk.document_id+" "+c.chunk.title+" "+" ".join(c.chunk.tags)
            exact=len(q&set(tokenize(haystack)))/max(1,len(q))
            authority={"public_reference":.09,"runbook":.08,"troubleshooting":.07,"community_support":.06,"incident":.06,"release_note":.05}.get(c.chunk.document_type,0)
            section=c.chunk.section_title.lower(); intent_boost=0.0
            if c.chunk.document_type=="community_support" and "accepted answer" in section: intent_boost+=.08
            if "source and attribution" in section: intent_boost-=.60
            if q&{"why","cause","caused","reason"}:
                if any(term in section for term in ["root cause","investigation"]): intent_boost+=1.20
                elif "summary" in section: intent_boost+=.45
            if q&{"fix","fixed","resolve","resolved","how","resolution"} and any(term in section for term in ["resolution","recovery","remediation"]): intent_boost+=.42
            if "verification" in q and "verification" in section: intent_boost+=.30
            matched_code=any(code in haystack.lower() for code in q_codes)
            if matched_code: intent_boost+=.45
            elif q_codes: intent_boost-=.45
            title_terms=set(tokenize(c.chunk.title)); title_overlap=len(q&title_terms)/max(1,len(q))
            if "stripe" in q and "stripe" not in set(tokenize(haystack)): intent_boost-=.60
            if "paypal" in q and "paypal" not in set(tokenize(haystack)): intent_boost-=.60
            c.reranker_score=exact+(1.4*title_overlap)+authority+intent_boost+c.score
        candidates.sort(key=lambda x:x.reranker_score or 0,reverse=True)
        for rank,item in enumerate(candidates[:top_k],1): item.final_rank=rank
        return candidates[:top_k]
