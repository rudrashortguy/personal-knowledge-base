import chromadb
from sentence_transformers import SentenceTransformer
from config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_dir)
        self.model = SentenceTransformer(settings.model_name)
        self.collection = self.client.get_or_create_collection("documents")

    def add_documents(self, chunks: list, doc_id: str):
        if not chunks:
            return
        texts = [c.page_content for c in chunks]
        metas = [c.metadata for c in chunks]
        ids = [f"{doc_id}_{c.metadata['chunk']}" for c in chunks]
        embeds = self.model.encode(texts).tolist()
        self.collection.add(embeddings=embeds, documents=texts, metadatas=metas, ids=ids)

    def search(self, query: str, k: int = 5) -> list:
        q_emb = self.model.encode([query]).tolist()[0]
        results = self.collection.query(query_embeddings=[q_emb], n_results=k)
        out = []
        for i in range(len(results['ids'][0])):
            out.append({
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
            })
        return out

    def delete_document(self, doc_id: str):
        self.collection.delete(where={"doc_id": doc_id})

    def list_documents(self) -> list:
        metas = self.collection.get(include=["metadatas"])
        seen = {}
        for m in metas["metadatas"]:
            seen[m["doc_id"]] = m["source"]
        return [{"id": k, "filename": v} for k, v in seen.items()]

    def has_file(self, file_hash: str) -> bool:
        results = self.collection.get(where={"doc_id": file_hash}, limit=1)
        return len(results["ids"]) > 0

vector_store = VectorStore()
