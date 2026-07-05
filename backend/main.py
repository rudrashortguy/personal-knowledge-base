import os, uuid
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models import QueryRequest, QueryResponse
from ingest import chunk_document, file_hash
from vectorstore import vector_store
from llm import query_ollama

app = FastAPI(title="Personal Knowledge Base")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5175"], allow_methods=["*"], allow_headers=["*"])
os.makedirs(settings.upload_dir, exist_ok=True)

def process_file(path: str, doc_id: str):
    chunks = chunk_document(path, doc_id)
    vector_store.add_documents(chunks, doc_id)

@app.post("/upload")
async def upload(files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    results = []
    for file in files:
        path = os.path.join(settings.upload_dir, f"{uuid.uuid4()}_{file.filename}")
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
        fhash = file_hash(path)
        if vector_store.has_file(fhash):
            os.remove(path)
            results.append({"filename": file.filename, "status": "already exists"})
            continue
        background_tasks.add_task(process_file, path, fhash)
        results.append({"filename": file.filename, "status": "processing"})
    return {"results": results}

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    results = vector_store.search(req.question)
    if not results:
        return QueryResponse(answer="No relevant documents found.", sources=[])
    context = "\n\n".join([f"[source: {r['metadata']['source']}, page {r['metadata']['page']}]\n{r['text']}" for r in results])
    answer = await query_ollama(req.question, context)
    sources = [{"filename": r["metadata"]["source"], "page": r["metadata"]["page"]} for r in results]
    return QueryResponse(answer=answer, sources=sources)

@app.get("/list-documents")
async def list_documents():
    return vector_store.list_documents()

@app.delete("/delete-document/{doc_id}")
async def delete_document(doc_id: str):
    vector_store.delete_document(doc_id)
    return {"status": "deleted"}

@app.get("/health")
async def health():
    return {"status": "ok"}
