import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ["KB_UPLOAD_DIR"] = "test_uploads"
os.environ["KB_CHROMA_DIR"] = "test_chroma"
