"""Run deterministic retrieval ablations and write honest JSON/CSV results."""
import csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"backend"))
from app.repository import KnowledgeRepository
from app.rag.pipeline import QueryAnalyzer
from app.retrieval import BM25Retriever,LocalSemanticRetriever,RerankerService,reciprocal_rank_fusion

def metrics(rows,k=5):
    n=len(rows); hits=recall=precision=mrr=ndcg=0.0
    for retrieved,expected in rows:
        expected=set(expected); top=retrieved[:k]; matches=[i for i,d in enumerate(top,1) if d in expected]
        if expected:
            hits+=bool(matches); recall+=len(set(top)&expected)/len(expected); precision+=len(set(top)&expected)/k
            if matches: mrr+=1/min(matches)
            dcg=sum(1/__import__('math').log2(i+1) for i,d in enumerate(top,1) if d in expected); ideal=sum(1/__import__('math').log2(i+1) for i in range(1,min(k,len(expected))+1)); ndcg+=dcg/ideal if ideal else 0
        else: hits+=not top
    return {"hit_rate@5":hits/n,"recall@5":recall/n,"precision@5":precision/n,"mrr":mrr/n,"ndcg@5":ndcg/n}
def run():
    repo=KnowledgeRepository(include_synthetic=True); questions=json.loads((ROOT/"data"/"evaluation"/"questions.json").read_text(encoding="utf-8")); bm=BM25Retriever(repo.chunks); dense=LocalSemanticRetriever(repo.chunks); analyzer=QueryAnalyzer(); configs={x:[] for x in ["dense","bm25","hybrid","hybrid_rewrite","hybrid_rewrite_rerank"]}
    for item in questions:
        q=item["question"]; expected=item["expected_document_ids"]
        dr=dense.search(q,20); br=bm.search(q,20); analysis=analyzer.analyze(q); hdr=reciprocal_rank_fusion([dense.search(analysis.rewritten_query,20),bm.search(analysis.rewritten_query,20)])
        candidates={"dense":dr,"bm25":br,"hybrid":reciprocal_rank_fusion([dr,br]),"hybrid_rewrite":hdr,"hybrid_rewrite_rerank":RerankerService().rerank(analysis.rewritten_query,hdr[:25],8)}
        for name,values in candidates.items(): configs[name].append(([v.chunk.document_id for v in values],expected))
    result={"dataset_size":len(questions),"note":"Deterministic local TF-IDF fallback; rerun after Qdrant ingestion for production-model results.","configurations":[{"retriever":name,**{k:round(v,4) for k,v in metrics(rows).items()}} for name,rows in configs.items()]}
    out=ROOT/"evaluation"/"results"; out.mkdir(parents=True,exist_ok=True); (out/"summary.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    with (out/"summary.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=result["configurations"][0].keys()); writer.writeheader(); writer.writerows(result["configurations"])
    print(json.dumps(result,indent=2))
if __name__=="__main__": run()
