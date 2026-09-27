from pathlib import Path
from fastapi.testclient import TestClient
import app.main as main_module
from app.ingestion.chunker import chunk_markdown
from app.ingestion.parser import parse_frontmatter
from app.main import app
from app.rag.pipeline import QueryAnalyzer,validate_citations
from app.retrieval import BM25Retriever,RerankerService,reciprocal_rank_fusion
from app.schemas import Chunk,RankedChunk

def chunk(cid,text,service="payment-service"):
    return Chunk(chunk_id=cid,document_id="DOC-1",title="Guide",section_title="Test",text=text,service=service)
def test_frontmatter_and_structure_aware_chunking():
    meta,body=parse_frontmatter("---\ndocument_id: DOC-1\ntags: [a, b]\n---\n# Title\n\nBody")
    assert meta["document_id"]=="DOC-1" and meta["tags"]==["a","b"]
    chunks=chunk_markdown({"document_id":"DOC-1","title":"Test"},"# Title\n\nIntro\n\n## Diagnosis\n\nEvidence")
    assert [c.section_title for c in chunks]==["Title","Diagnosis"]
def test_query_analyzer_preserves_identifiers_and_filters():
    result=QueryAnalyzer().analyze("Why does my PostgreSQL 16 database reject a connection in production?")
    assert result.entities.technologies==["PostgreSQL 16", "PostgreSQL"]
    assert result.filters=={"service":"database"} and "PostgreSQL" in result.rewritten_query
def test_bm25_exact_identifier_and_metadata_filter():
    retriever=BM25Retriever([chunk("a","DB-104 database pool timeout"),chunk("b","DB-104 order replay","order-service")])
    assert retriever.search("DB-104",filters={"service":"payment-service"})[0].chunk.chunk_id=="a"
def test_rrf_uses_rank_not_raw_score():
    a,b=chunk("a","alpha"),chunk("b","beta")
    fused=reciprocal_rank_fusion([[RankedChunk(chunk=a,rank=1,score=.01,dense_rank=1),RankedChunk(chunk=b,rank=2,score=.99,dense_rank=2)],[RankedChunk(chunk=a,rank=2,bm25_rank=2),RankedChunk(chunk=b,rank=1,bm25_rank=1)]],60)
    assert len(fused)==2 and round(fused[0].score,8)==round(fused[1].score,8)
def test_reranker_and_citation_validation():
    candidate=RankedChunk(chunk=chunk("a","DB-104 payment database timeout"),rank=1,score=.02)
    assert RerankerService().rerank("DB-104 payment",[candidate])[0].reranker_score>0
    answer,validity,coverage=validate_citations("Supported [DOC-1], invented [DOC-999].",[candidate])
    assert "DOC-999" not in answer and validity==.5 and coverage==1
def test_api_health_documents_and_query():
    client=TestClient(app)
    health=client.get("/api/health"); assert health.status_code==200 and health.json()["document_count"]>=190
    response=client.post("/api/query",json={"query":"PostgreSQL says password authentication failed for user postgres. What should I check?"})
    assert response.status_code==200; data=response.json(); assert data["sources"] and data["retrieval_debug"]["fused_results"]
    assert data["response_id"].startswith("resp_") and data["conversation_id"].startswith("conv_")

def test_vague_problem_returns_guided_clarification_not_an_unrelated_fix():
    client=TestClient(app)
    response=client.post("/api/query",json={"query":"The payment page doesnt work, what should I do?","debug":False})
    data=response.json()
    assert response.status_code==200 and not data["sources"]
    assert "Check these first" in data["answer"] and "Network request" in data["answer"]

def test_frontend_crash_clarification_stays_in_the_frontend_domain():
    client=TestClient(app)
    response=client.post("/api/query",json={"query":"The website keeps crashing on the client side. Why?","debug":False})
    data=response.json()
    assert not data["sources"] and "JavaScript runtime exception" in data["answer"]
    assert "payment provider" not in data["answer"].lower()

def test_payment_reconciliation_answer_is_clear_and_not_polluted_by_auth_results():
    client=TestClient(app)
    response=client.post("/api/query",json={"query":"Customers are charged successfully, but their orders remain marked as unpaid. What should I investigate?","debug":False})
    data=response.json()
    assert data["evidence_support"]=="General diagnostic guidance" and not data["sources"]
    assert "payment-to-order reconciliation failure" in data["answer"]
    assert "Cognito" not in data["answer"] and "Google" not in data["answer"]

def test_missing_payment_button_gets_frontend_deployment_playbook():
    client=TestClient(app)
    response=client.post("/api/query",json={"query":"The payment button disappeared after a frontend deployment. What should I inspect first?","debug":False})
    data=response.json()
    assert "JavaScript exception" in data["answer"] and "payment SDK" in data["answer"]
    assert data["evidence_support"]=="General diagnostic guidance"

def test_ai_status_and_follow_up_history_contract():
    client=TestClient(app)
    status=client.get("/api/ai/status")
    assert status.status_code==200 and isinstance(status.json()["connected"],bool)
    first=client.post("/api/query",json={"query":"The payment button disappeared after deployment.","debug":False}).json()
    second=client.post("/api/query",json={"query":"The console now says the SDK is undefined.","conversation_id":first["conversation_id"],"history":[{"role":"user","content":"The payment button disappeared after deployment."},{"role":"assistant","content":first["answer"]}],"debug":False})
    assert second.status_code==200 and second.json()["conversation_id"]==first["conversation_id"]

def test_feedback_is_saved_locally(tmp_path):
    client=TestClient(app); old_root=main_module.settings.project_root
    main_module.settings.project_root=tmp_path
    try:
        response=client.post("/api/feedback",json={"response_id":"resp_12345678","conversation_id":"conv_12345678","helpful":False,"comment":"Needs a clearer first step."})
        assert response.status_code==200 and (tmp_path/"data"/"feedback.jsonl").read_text(encoding="utf-8").count("Needs a clearer first step.")==1
    finally: main_module.settings.project_root=old_root

def test_text_document_upload_is_indexed(tmp_path):
    client=TestClient(app); old_root=main_module.settings.project_root; old_raw=main_module.repository.raw_dir
    main_module.settings.project_root=tmp_path; main_module.repository.raw_dir=tmp_path/"data"/"raw"
    try:
        response=client.post("/api/documents/upload",data={"title":"Checkout Operations Guide","service":"payments"},files={"file":("guide.txt",b"Checkout recovery guide.\n\nIf a webhook fails, inspect its delivery status and retry history before reconciling the order.","text/plain")})
        assert response.status_code==200 and response.json()["document_id"].startswith("UPL-")
        assert any(doc.title=="Checkout Operations Guide" for doc in main_module.repository.documents.values())
    finally:
        main_module.settings.project_root=old_root; main_module.repository.raw_dir=old_raw; main_module.repository.load()
