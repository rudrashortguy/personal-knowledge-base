# Deployment

## Hardware Requirements
- **RAM**: 2GB minimum (embeddings grow with documents)
- **Disk**: ChromaDB stores vectors; ~100MB per 1000 pages

## Dependencies
- Tesseract OCR: `brew install tesseract` (macOS) or `apt install tesseract-ocr` (Linux)
- Ollama with `gemma2:latest` pulled
- Python 3.12+
- Node.js 20+

## Local Setup
```bash
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
./run.sh
```

## Docker
```bash
docker compose up --build
```

## Notes
- ChromaDB persists to `chroma_db/` directory; mount as volume in Docker.
- Embedding model downloads on first run (~90MB).
- Not suitable for free cloud tiers (sentence-transformers + ChromaDB are too heavy).
