import httpx, json
from config import settings

OLLAMA_URL = f"{settings.ollama_base_url}/api/generate"

SYSTEM_PROMPT = """You are a Q&A assistant with access to retrieved document chunks. Answer using ONLY the provided context. Always cite sources as [source: filename, page X]. If the context doesn't contain enough info, say so."""

async def query_ollama(question: str, context: str) -> str:
    prompt = f"Question: {question}\n\nContext:\n{context}"
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {"temperature": 0.1},
    }
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()
        return resp.json()["response"]
