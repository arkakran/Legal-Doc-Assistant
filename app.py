import os
import time
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

from utils.read_data import load_all_pdfs
from utils.preprocess_data import preprocess_documents
from utils.chunking_data import chunk_documents
from utils.create_embeddings import Embeddings
from utils.vector_database import VectorDB
from utils.retrieval_qa import RetrievalQA

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")

# Embedding cache filename (stored inside VECTOR_DIR)
EMB_CACHE_NAME = "embeddings_all_mpnet_base_v2.npz"

app = Flask(__name__)

# Initialize VectorDB (HNSW + cosine via normalization)
vdb = VectorDB(VECTOR_DIR)

if not vdb.exists():
    print("Building FAISS HNSW index from PDFs...")
    t0 = time.time()

    # 1) Load
    docs = load_all_pdfs(DATA_DIR)
    print(f"- Loaded pages: {len(docs)}")

    # 2) Preprocess
    docs = preprocess_documents(docs)
    print("- Preprocessed documents")

    # 3) Chunk
    chunks = chunk_documents(
        docs,
        chunk_size=3000,
        chunk_overlap=300,
        separators=["\n\n", "\n", "Section ", "SECTION ", "Sec. ", "CHAPTER ", "Chapter ", " "]
    )
    print(f"- Total chunks: {len(chunks)}")

    # 4) Embeddings (with caching)
    embeddings = Embeddings("sentence-transformers/all-mpnet-base-v2")
    print("- Computing/loading embeddings (will cache to disk) ...")
    vdb.build(
        embeddings,
        chunks,
        hnsw_M=16,
        hnsw_ef_construction=100,
        hnsw_ef_search=64,
        cache_name=EMB_CACHE_NAME,     # save embeddings to VECTOR_DIR/EMB_CACHE_NAME
        force_recompute=False          # set True only if PDFs or chunking changed
    )
    print(f"Index build completed in {time.time() - t0:.1f}s.")
else:
    print("Loading existing FAISS HNSW index...")
    vdb.load()
    # Increase recall at query time
    try:
        vdb.set_search_params(ef_search=128)
        print("- Set efSearch=128 for higher recall")
    except Exception:
        pass

qa = RetrievalQA(vdb, embed_model_name="sentence-transformers/all-mpnet-base-v2")

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/health")
def health():
    return jsonify({"status": "OK"})

@app.route("/logs")
def logs():
    return jsonify({"logs": ["System started", "Index loaded", "User asked: sample question"]})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    query = (data.get("question") or "").strip()
    if not query:
        return jsonify({"error": "Empty question"}), 400

    answer, hits = qa.ask(query, top_k=6, max_tokens=800)

    # Clean sources: keep only PDF file name, not full path
    cleaned_hits = []
    for h in hits:
        meta = h.get("meta", {}).copy()
        if "source" in meta:
            meta["source"] = os.path.basename(meta["source"])  # <-- only filename
        cleaned_hits.append({
            "rank": h.get("rank"),
            "score": h.get("score"),
            "text": h.get("text"),
            "meta": meta
        })

    return jsonify({"answer": answer, "sources": cleaned_hits})


if __name__ == "__main__":
    # For Windows users seeing long initial build times:
    # - First run builds & caches embeddings + index
    # - Next runs will start fast and set efSearch=128 automatically
    app.run(host="0.0.0.0", port=7860, debug=True)
