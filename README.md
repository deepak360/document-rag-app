# Document Management & RAG-based Q&A Backend - document-rag-app

A production-ready backend application for document ingestion and retrieval-augmented question answering (RAG)

## Features
- FastAPI async backend
- User Authentication & Signup APIs
- Document upload & text extraction
- Retrieval-Augmented Generation Q&A
- PostgreSQL + SQLAlchemy async
- LLM support: Langchain / OpenAI / HuggingFace
- Dockerized and CI/CD-ready
- 70%+ test coverage with pytest

## 📁 Architecture
```
User ─► FastAPI ─► DocumentIngestionAPI
                     │
                     ├──► Langchain (OpenAI/HF/TfidfVectorizer/ollama) Embedding
                     ├──► PostgreSQL Embedding Storage (pgvector)
                     └──► QA API ─► Retriever ─► Answer via RAG
```

## Setup Instructions

### Local Development
```bash
# Clone the repo
$ git clone <your_repo_url>
$ cd project_root

# Create virtual env and activate
$ python3 -m venv env
$ source env/bin/activate

# Install dependencies
$ pip3 install -r requirements.txt

# Change .env.local to .env

# Run app
$ uvicorn app.main:app --reload
```

### With Docker
```bash
# Start all services
$ docker compose up --build

# Start all test coverage
$ docker compose exec  backend pytest app/tests/ --cov=app

# Swagger based documentation
$ http://127.0.0.1:8000/docs
```

## API Endpoints
- `POST /ingest/` — Upload document, generate embedding
- `POST /qa/` — Ask question, get answer
- `GET /select/` — Choose which documents to include

## Run Tests
```bash
# Run tests with coverage
$ pytest --cov=app
```

## CI/CD
- GitHub Actions (`.github/workflows/ci.yml`)
- Runs tests and builds on each PR (This needs to be done)

## LLM Integration
- Using Langchain interface
- Plug in ollama/TfidfVectorizer (OpenAI or Hugging Face) easily via environment/config

## Environment Variables (`.env`)
```
DATABASE_URL=postgresql+asyncpg://user:pass@db/ragdb
```

##  Alembic
```
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
alembic revision --autogenerate -m "Initial migration"
```

## open postgres shell inside docker
```
docker exec -it 3c91d5d56064 psql -U newuser ragdb
```

## For localhost specific error
```
export DOCKER_HOST=unix:///var/run/docker.sock
```
##  Error when port bind on localhost
```
 sudo service postgresql stop
 ```