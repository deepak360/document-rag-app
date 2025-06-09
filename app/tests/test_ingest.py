import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_document_ingestion():
    test_doc = {
        "doc_id": "doc_008",
        "title": "Testing Ingestion",
        "content": "This document is for ingestion test in the RAG application."
    }

    async with AsyncClient(base_url="http://backend:8000", follow_redirects=True) as ac:
        response = await ac.post("/ingest", json=test_doc)

    print("RESPONSE STATUS:", response.status_code)
    print("RESPONSE BODY:", response.text)

    assert response.status_code in (200, 201)
