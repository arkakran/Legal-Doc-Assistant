# from sentence_transformers import SentenceTransformer
# import numpy as np

# class Embeddings:
#     def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
#         self.model = SentenceTransformer(model_name)

#     def encode(self, texts, batch_size=64, normalize=True):
#         vecs = self.model.encode(
#             texts,
#             batch_size=batch_size,
#             show_progress_bar=True,
#             normalize_embeddings=normalize
#         )
#         return vecs.astype(np.float32)


# utils/create_embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
import os

class Embeddings:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, batch_size=64, normalize=True, show_progress=True):
        vecs = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=normalize
        )
        return vecs.astype(np.float32)

    def cache_path(self, vector_dir, cache_name="embeddings_all_mpnet_base_v2.npz"):
        os.makedirs(vector_dir, exist_ok=True)
        return os.path.join(vector_dir, cache_name)

    def save_embeddings(self, vector_dir, embeddings: np.ndarray, meta: dict, cache_name=None):
        """
        Saves embeddings and lightweight metadata:
        - embeddings: np.ndarray (N, D)
        - meta: dict with keys you care about (e.g., {'model': model_name, 'count': N})
        """
        path = self.cache_path(vector_dir, cache_name or f"embeddings_{self.model_name.replace('/', '_')}.npz")
        np.savez_compressed(path, vectors=embeddings, **meta)
        return path

    def load_embeddings(self, vector_dir, cache_name=None):
        """
        Returns (embeddings: np.ndarray, meta: dict) or (None, None) if not found.
        """
        path = self.cache_path(vector_dir, cache_name or f"embeddings_{self.model_name.replace('/', '_')}.npz")
        if not os.path.exists(path):
            return None, None
        data = np.load(path, allow_pickle=True)
        vectors = data["vectors"]
        # collect any other saved meta keys
        meta = {k: data[k].item() if data[k].shape == () else data[k] for k in data.files if k != "vectors"}
        return vectors, meta

    def get_or_build(self, texts, vector_dir, batch_size=64, normalize=True, show_progress=True, cache_name=None, force_recompute=False):
        """
        Main entry-point:
        - Try to load cached embeddings
        - If missing or force_recompute=True, compute and save
        """
        if not force_recompute:
            cached, meta = self.load_embeddings(vector_dir, cache_name)
            if cached is not None and cached.shape[0] == len(texts):
                return cached

        vectors = self.encode(texts, batch_size=batch_size, normalize=normalize, show_progress=show_progress)
        meta = {
            "model": self.model_name,
            "count": int(vectors.shape),
            "dim": int(vectors.shape[1]),
        }
        self.save_embeddings(vector_dir, vectors, meta, cache_name)
        return vectors
