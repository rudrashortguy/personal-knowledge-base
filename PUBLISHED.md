# Personal Knowledge Base — Published

**Repository**: https://github.com/rudrashortguy/personal-knowledge-base
**Release**: v1.0.0

## Hardware Requirements
- Ollama with `gemma2:latest` (4GB+ RAM)
- Tesseract OCR
- 2GB+ RAM for sentence-transformers + ChromaDB
- Python 3.12+ and Node.js 20+

## Quick Start
```bash
./run.sh                    # Backend on :8002, Frontend on :5175
```
Or Docker:
```bash
docker compose up --build
```

Not suitable for free cloud tiers (too heavy).
