.PHONY: setup infrastructure corpus ingest backend frontend evaluate test
setup:
	python -m pip install -r backend/requirements.txt
	cd frontend && npm install
infrastructure:
	docker compose up -d qdrant
corpus:
	python scripts/generate_corpus.py
ingest:
	python scripts/ingest.py
backend:
	cd backend && uvicorn app.main:app --reload
frontend:
	cd frontend && npm run dev
evaluate:
	python scripts/evaluate.py
test:
	cd backend && pytest
