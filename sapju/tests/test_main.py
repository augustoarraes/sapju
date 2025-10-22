import pytest
from httpx import AsyncClient, ASGITransport
from app.api import app

transport = ASGITransport(app=app)
base_url = "http://api"


@pytest.mark.asyncio
async def test_read_ping():
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        res = await ac.get("/ping")
        assert res.status_code == 200
        assert res.json() == {"ping": "pong"}


@pytest.mark.asyncio
async def teste_cadastro_processo():
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        res = await ac.post("/api/processos", json={"classe": "AI", "numero": 9090, "orgao_origem": "STJ"})
        assert res.status_code == 201
        assert res.json() == {"status": "processo cadastrado"}



