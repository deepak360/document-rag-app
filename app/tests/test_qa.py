import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_retrieve_documents():
    async with AsyncClient(base_url="http://backend:8000", follow_redirects=True) as ac:
        response = await ac.post("/qa", json={"question": "Great Wall of China"})

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
