import os
from langchain_community.document_loaders import PyPDFLoader

def load_all_pdfs(data_dir: str):
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Directory not found: {data_dir}")

    pdf_names = [n for n in os.listdir(data_dir) if n.lower().endswith(".pdf")]
    if not pdf_names:
        raise FileNotFoundError(f"No PDFs found in: {data_dir}")

    docs = []
    for name in pdf_names:
        path = os.path.join(data_dir, name)
        try:
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        except Exception as e:
            print(f"Warning: failed to load {name}: {e}")
    return docs
