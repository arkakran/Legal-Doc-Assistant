import re

def clean_text(t: str) -> str:
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'\bPage\s*\d+\b', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\b\d+\s*/\s*\d+\b', '', t)   # 3/25 style page markers
    return t

def preprocess_documents(docs):
    for d in docs:
        d.page_content = clean_text(d.page_content)
    return docs
