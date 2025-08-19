import os
import pickle
import faiss
import numpy as np

class VectorDB:
    def __init__(self, vector_dir: str):
        self.vector_dir = vector_dir
        os.makedirs(vector_dir, exist_ok=True)

        self.index_path = os.path.join(vector_dir, "faiss_hnsw_index.faiss")
        self.meta_path  = os.path.join(vector_dir, "faiss_hnsw_meta.pkl")

        self.index = None
        self.texts = None
        self.metas = None
        self.dim = None

    def exists(self):
        return os.path.exists(self.index_path) and os.path.exists(self.meta_path)

    def build(self, embeddings, chunks, hnsw_M=16, hnsw_ef_construction=100, hnsw_ef_search=64, cache_name=None, force_recompute=False):
        # Prepare corpus
        texts = [c.page_content for c in chunks]
        metas = [c.metadata for c in chunks]

        # 1) Try cache first, else compute then save via get_or_build
        embs = embeddings.get_or_build(
            texts=texts,
            vector_dir=self.vector_dir,
            batch_size=32,            # safe on CPU; adjust if you have more RAM/cores
            normalize=True,           # keep normalized for cosine
            show_progress=True,
            cache_name=cache_name,    # e.g., "embeddings_all_mpnet_base_v2.npz"
            force_recompute=force_recompute
        ).astype(np.float32)

        dim = embs.shape[1]

        # 2) Build HNSW
        index = faiss.IndexHNSWFlat(dim, hnsw_M)
        index.hnsw.efConstruction = hnsw_ef_construction
        index.hnsw.efSearch = hnsw_ef_search
        index.add(embs)

        # 3) Persist
        faiss.write_index(index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump({"texts": texts, "metas": metas, "dim": dim}, f)

        # 4) Set in-memory
        self.index, self.texts, self.metas, self.dim = index, texts, metas, dim

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, "rb") as f:
            data = pickle.load(f)
        self.texts = data["texts"]
        self.metas = data["metas"]
        self.dim   = data.get("dim", None)
        # Good recall at query time:
        try:
            self.index.hnsw.efSearch = 128
        except Exception:
            pass

    def set_search_params(self, ef_search: int = None):
        if ef_search is not None:
            self.index.hnsw.efSearch = ef_search

    # def search(self, query_emb: np.ndarray, top_k=6):
    #     D, I = self.index.search(query_emb.astype(np.float32), top_k)
    #     hits = []
    #     for r, idx in enumerate(I[0]):
    #         hits.append({
    #             "rank": r+1,
    #             "score": float(D[r]),
    #             "text": self.texts[idx],
    #             "meta": self.metas[idx]
    #         })
    #     return hits


    def search(self, query_emb: np.ndarray, top_k=6):
        # Ensure 2D float32 (nq, d)
        if isinstance(query_emb, list):
            query_emb = np.array(query_emb, dtype=np.float32)
        if query_emb.ndim == 1:
            query_emb = query_emb[None, :]
        q = query_emb.astype(np.float32, copy=False)

        D, I = self.index.search(q, top_k)

        # Guard: empty results
        if D is None or I is None or D.size == 0 or I.size == 0:
            return []

    # Take first query row and flatten to 1D arrays of native types
        drow = np.asarray(D[0]).reshape(-1)
        irow = np.asarray(I).reshape(-1)

    # Convert to Python types to avoid scalar casting issues
        drow = [float(x) for x in drow]
        irow = [int(x) for x in irow]

        hits = []
        for r, (score, idx) in enumerate(zip(drow, irow), start=1):
            # FAISS can return -1 when not enough neighbors
            if idx < 0 or idx >= len(self.texts):
                continue
            hits.append({
                "rank": r,
                "score": score,
                "text": self.texts[idx],
                "meta": self.metas[idx]
            })
        return hits
































