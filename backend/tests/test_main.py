import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_list_docs_empty(client):
    r = await client.get("/list-documents")
    assert r.status_code == 200

@pytest.mark.asyncio
async def test_query_no_docs(client):
    r = await client.post("/query", json={"question": "test"})
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
