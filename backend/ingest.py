import os, hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import settings

text_splitter = RecursiveCharacterTextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)

EXTRACTORS = {}

def _txt(path):
    with open(path) as f:
        return f.read()
EXTRACTORS['.txt'] = _txt
EXTRACTORS['.md'] = _txt

def _pdf(path):
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(path)
    pages = []
    for i in range(len(doc)):
        pages.append(doc[i].get_text_bounded())
    return "\n\n".join(pages)
EXTRACTORS['.pdf'] = _pdf

def _docx(path):
    import docx2txt
    return docx2txt.process(path)
EXTRACTORS['.docx'] = _docx

def _image(path):
    from PIL import Image
    import pytesseract
    return pytesseract.image_to_string(Image.open(path))
EXTRACTORS['.png'] = _image
EXTRACTORS['.jpg'] = _image
EXTRACTORS['.jpeg'] = _image

def extract_text(path: str) -> str:
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    fn = EXTRACTORS.get(ext)
    if fn:
        return fn(path)
    return ""

def chunk_document(path: str, doc_id: str) -> list[Document]:
    text = extract_text(path)
    if not text:
        return []
    chunks = text_splitter.split_text(text)
    docs = []
    for i, chunk in enumerate(chunks):
        docs.append(Document(
            page_content=chunk,
            metadata={"source": os.path.basename(path), "doc_id": doc_id, "chunk": i, "page": i + 1},
        ))
    return docs

def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()
