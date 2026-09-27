import json
import re
import time
import uuid
from datetime import date, datetime, timezone
from io import BytesIO
from collections import Counter
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.rag.pipeline import ContextBuilder, GroqLLM, MockLLM, OllamaLLM, QueryAnalyzer, evidence_label, find_ollama_model, needs_clarification, playbook_answer, validate_citations
from app.repository import repository
from app.retrieval import BM25Retriever, LocalSemanticRetriever, QdrantVectorRetriever, RerankerService, reciprocal_rank_fusion
from app.retrieval.pipeline import tokenize
from app.schemas import AIStatus, Citation, FeedbackRequest, FeedbackResponse, HealthResponse, QueryRequest, QueryResponse

settings=get_settings(); app=FastAPI(title="ResolveAI API",version="1.0.0",description="Explainable enterprise hybrid RAG")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_methods=["*"],allow_headers=["*"])
query_count=0; latencies=[]

def _active_llm():
    provider=settings.llm_provider.lower()
    if provider in {"auto","ollama"}:
        model=find_ollama_model(settings.ollama_url,settings.llm_model)
        if model: return OllamaLLM(settings.ollama_url,model),"AI synthesis","ollama",model
    if provider in {"auto","groq"} and settings.groq_api_key and settings.llm_model:
        return GroqLLM(settings.groq_api_key,settings.llm_model),"AI synthesis","groq",settings.llm_model
    return MockLLM(),"Guided fallback","guided",""

def _pipeline(request:QueryRequest)->QueryResponse:
    global query_count
    started=time.perf_counter(); timings={}; analyzer=QueryAnalyzer(); t=time.perf_counter(); analysis=analyzer.analyze(request.query); timings["analysis_ms"]=(time.perf_counter()-t)*1000
    bm25=BM25Retriever(repository.chunks)
    try: dense=QdrantVectorRetriever(repository.chunks,settings.qdrant_url,settings.embedding_model)
    except Exception: dense=LocalSemanticRetriever(repository.chunks)
    dense_all=[]; sparse_all=[]; t=time.perf_counter()
    for q in analysis.subqueries: dense_all.append(dense.search(q,settings.top_k_dense,analysis.filters))
    timings["dense_ms"]=(time.perf_counter()-t)*1000; t=time.perf_counter()
    for q in analysis.subqueries: sparse_all.append(bm25.search(q,settings.top_k_bm25,analysis.filters))
    timings["bm25_ms"]=(time.perf_counter()-t)*1000
    dense_fused=reciprocal_rank_fusion(dense_all,settings.rrf_k); sparse_fused=reciprocal_rank_fusion(sparse_all,settings.rrf_k)
    if len(dense_fused)+len(sparse_fused)<6 and analysis.filters:
        analysis.filters={}; dense_fused=reciprocal_rank_fusion([dense.search(q,settings.top_k_dense) for q in analysis.subqueries],settings.rrf_k); sparse_fused=reciprocal_rank_fusion([bm25.search(q,settings.top_k_bm25) for q in analysis.subqueries],settings.rrf_k)
    t=time.perf_counter(); fused=reciprocal_rank_fusion([dense_fused,sparse_fused],settings.rrf_k)[:25]; timings["fusion_ms"]=(time.perf_counter()-t)*1000
    t=time.perf_counter(); reranked=RerankerService().rerank(request.query,fused,settings.top_k_rerank)
    query_words={word for word in tokenize(request.query) if len(word)>2 and word not in {"what","when","where","which","should","does","with","from","this","that"}}
    title_matches=[]
    for item in reranked:
        title_words=set(tokenize(item.chunk.title)); overlap=len(query_words&title_words)/max(1,len(query_words))
        title_matches.append((overlap,item.chunk.document_id))
    best_title,best_document=max(title_matches,default=(0,""))
    if best_title>=.55:
        exact_document=[item for item in fused if item.chunk.document_id==best_document]
        reranked=RerankerService().rerank(request.query,exact_document,settings.top_k_rerank)
    selected=ContextBuilder().select(reranked,settings.top_k_rerank)
    stop={"what","why","which","when","where","does","did","have","with","after","from","start","started","upgrading","upgrade","nexora","service","provider","the","and","use"}
    salient={x for x in tokenize(request.query) if x not in stop and len(x)>2}; evidence_tokens=set(tokenize(" ".join(x.chunk.text for x in selected)))
    playbook=playbook_answer(request.query); llm,answer_mode,_,_=_active_llm()
    if (playbook and answer_mode=="Guided fallback") or needs_clarification(request.query) or (salient and len(salient&evidence_tokens)/len(salient)<.5): selected=[]
    timings["rerank_context_ms"]=(time.perf_counter()-t)*1000
    history=[turn.model_dump() for turn in request.history[-8:]]; t=time.perf_counter()
    try: answer=llm.generate(request.query,selected,history) if answer_mode=="AI synthesis" else (playbook or llm.generate(request.query,selected,history))
    except Exception:
        answer_mode="Guided fallback"; answer=playbook or MockLLM().generate(request.query,selected,history)
    timings["generation_ms"]=(time.perf_counter()-t)*1000; answer,validity,coverage=validate_citations(answer,selected); label,explanation=evidence_label(selected,validity)
    if (playbook and answer_mode=="Guided fallback") or not selected: label,explanation="General diagnostic guidance","A structured investigation path is provided without claiming that a specific root cause has been confirmed."
    citations=[Citation(document_id=c.chunk.document_id,title=c.chunk.title,section=c.chunk.section_title) for c in selected if f"[{c.chunk.document_id}]" in answer]
    elapsed=(time.perf_counter()-started)*1000; timings["total_ms"]=elapsed; query_count+=1; latencies.append(elapsed)
    debug={"original_query":analysis.original_query,"rewritten_query":analysis.rewritten_query,"intent":analysis.intent,"entities":analysis.entities.model_dump(),"subqueries":analysis.subqueries,"metadata_filters":analysis.filters,"filter_strategy":"strict then relaxed when fewer than six candidates","dense_results":[x.model_dump() for x in dense_fused[:10]],"bm25_results":[x.model_dump() for x in sparse_fused[:10]],"fused_results":[x.model_dump() for x in fused[:15]],"selected_context":[x.model_dump() for x in selected],"timings":timings}
    return QueryResponse(response_id=f"resp_{uuid.uuid4().hex}",conversation_id=request.conversation_id or f"conv_{uuid.uuid4().hex}",answer=answer,citations=citations,sources=selected,evidence_support=label,evidence_explanation=explanation,citation_validity=validity,source_coverage=coverage,latency_ms=elapsed,answer_mode=answer_mode,retrieval_debug=debug if request.debug else None)

@app.get("/api/health",response_model=HealthResponse)
def health(): return HealthResponse(status="ok",corpus_loaded=bool(repository.documents),document_count=len(repository.documents),chunk_count=len(repository.chunks),vector_backend="local-tfidf-fallback (Qdrant configured)",llm_provider=settings.llm_provider)
@app.get("/api/ai/status",response_model=AIStatus)
def ai_status():
    _,mode,provider,model=_active_llm()
    connected=mode=="AI synthesis"
    message=(f"Connected to {provider.title()} using {model}." if connected else "No AI model is connected. Answers use the built-in guided fallback until Ollama or Groq is configured.")
    return AIStatus(provider=provider,model=model,connected=connected,message=message)
@app.post("/api/query",response_model=QueryResponse)
@app.post("/api/query/debug",response_model=QueryResponse)
def query(request:QueryRequest): return _pipeline(request)
@app.get("/api/documents")
def documents(document_type:str|None=None,service:str|None=None): return [d for d in repository.summaries() if (not document_type or d.document_type==document_type) and (not service or d.service==service)]
@app.get("/api/documents/{document_id}")
def document(document_id:str):
    if document_id not in repository.documents: raise HTTPException(404,"Document not found")
    return repository.documents[document_id]
@app.get("/api/incidents")
def incidents(): return [d for d in repository.summaries() if d.document_type in {"incident","community_support"}]
@app.post("/api/ingest")
def ingest(): repository.load(); return {"status":"indexed","documents":len(repository.documents),"chunks":len(repository.chunks)}
@app.post("/api/documents/upload")
async def upload_document(file:UploadFile=File(...),title:str=Form(""),service:str=Form("general")):
    suffix=(file.filename or "").lower().rsplit(".",1)[-1]
    if suffix not in {"md","txt","pdf"}: raise HTTPException(400,"Upload a Markdown, text, or PDF document.")
    payload=await file.read()
    if not payload or len(payload)>5_000_000: raise HTTPException(400,"The document must be between 1 byte and 5 MB.")
    try:
        if suffix=="pdf":
            from pypdf import PdfReader
            content="\n\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(payload)).pages)
        else: content=payload.decode("utf-8")
    except Exception as exc: raise HTTPException(400,"The document could not be read. Use a text-based PDF, Markdown, or UTF-8 text file.") from exc
    content=content.strip()
    if len(content)<40: raise HTTPException(400,"The document does not contain enough readable text.")
    safe_title=(title.strip() or re.sub(r"[-_]"," ",(file.filename or "Uploaded document").rsplit(".",1)[0]).title())[:160]
    safe_service=re.sub(r"[^a-z0-9-]+","-",service.strip().lower()).strip("-")[:50] or "general"
    document_id=f"UPL-{uuid.uuid4().hex[:10].upper()}"; upload_dir=settings.project_root/"data"/"raw"/"uploads"; upload_dir.mkdir(parents=True,exist_ok=True)
    quoted_title=safe_title.replace('"',"'")
    markdown=f'---\ndocument_id: {document_id}\ntitle: "{quoted_title}"\ndocument_type: uploaded_document\nservice: {safe_service}\nupdated_at: {date.today().isoformat()}\npublisher: Administrator upload\ntags: [uploaded]\n---\n\n# {safe_title}\n\n{content}\n'
    (upload_dir/f"{document_id.lower()}.md").write_text(markdown,encoding="utf-8"); repository.load()
    return {"status":"indexed","document_id":document_id,"title":safe_title,"chunk_count":repository.documents[document_id].chunk_count}
@app.post("/api/feedback",response_model=FeedbackResponse)
def save_feedback(request:FeedbackRequest):
    path=settings.project_root/"data"/"feedback.jsonl"; path.parent.mkdir(parents=True,exist_ok=True); record={**request.model_dump(),"created_at":datetime.now(timezone.utc).isoformat()}
    with path.open("a",encoding="utf-8") as handle: handle.write(json.dumps(record,ensure_ascii=False)+"\n")
    return FeedbackResponse()
@app.get("/api/evaluation/results")
def evaluation_results():
    path=settings.project_root/"evaluation"/"results"/"summary.json"
    if not path.exists(): return {"status":"not_run","configurations":[]}
    import json; return json.loads(path.read_text(encoding="utf-8"))
@app.get("/api/metrics")
def metrics(): return {"total_documents":len(repository.documents),"total_chunks":len(repository.chunks),"queries_processed":query_count,"average_query_latency_ms":round(sum(latencies)/len(latencies),2) if latencies else 0,"retrieval_strategy_distribution":{"hybrid_rrf_rerank":query_count},"services":Counter(c.service for c in repository.chunks)}

# Production uses one public URL: FastAPI serves both the API and compiled React app.
static_dir=settings.project_root/"frontend"/"dist"
if static_dir.exists():
    app.mount("/assets",StaticFiles(directory=static_dir/"assets"),name="assets")
    @app.get("/{full_path:path}",include_in_schema=False)
    def frontend(full_path:str):
        candidate=(static_dir/full_path).resolve()
        if candidate.is_file() and static_dir.resolve() in candidate.parents: return FileResponse(candidate)
        return FileResponse(static_dir/"index.html")
