# # utils/retrieval_qa.py
# from groq import Groq
# from .create_embeddings import Embeddings

# MODEL_NAME = "llama-3.3-70b-versatile"

# class RetrievalQA:
#     def __init__(self, vectordb, embed_model_name="sentence-transformers/all-mpnet-base-v2"):
#         self.vdb = vectordb
#         self.embeddings = Embeddings(embed_model_name)
#         self.client = Groq()  # reads GROQ_API_KEY from env

#     def ask(self, query: str, top_k=6, max_tokens=800, temperature=0.2):
#         # 1) Encode the query; ensure 2D shape (1, dim)
#         q_emb = self.embeddings.encode([query], normalize=True, show_progress=False)
#         if q_emb.ndim != 2 or q_emb.shape[0] != 1:
#             # Defensive guard: make sure it is (1, dim)
#             q_emb = q_emb.reshape(1, -1)

#         # 2) Retrieve
#         hits = self.vdb.search(q_emb, top_k=top_k)

#         # 3) Build context from hits (handle empty results)
#         if not hits:
#             context = "No relevant context found in the indexed documents."
#         else:
#             context = "\n\n".join([f"[{h['rank']}] {h['text']}" for h in hits])

#         # 4) Compose prompts
#         system_prompt = (
#             "You are a legal assistant. Answer based strictly on the provided Indian law context. "
#             "Cite relevant sections if present; if unclear, say you cannot find it in the context."
#         )
#         user_prompt = f"Question: {query}\n\nContext:\n{context}"

#         # 5) Call LLM
#         completion = self.client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt},
#             ],
#             temperature=temperature,
#             max_tokens=max_tokens,
#         )

#         answer = completion.choices[0].message.content if completion.choices else ""
#         return answer, hits



































# utils/retrieval_qa.py
from groq import Groq
from .create_embeddings import Embeddings

MODEL_NAME = "llama-3.3-70b-versatile"

class RetrievalQA:
    def __init__(self, vectordb, embed_model_name="sentence-transformers/all-mpnet-base-v2"):
        self.vdb = vectordb
        self.embeddings = Embeddings(embed_model_name)
        self.client = Groq()  # reads GROQ_API_KEY from env

    def ask(self, query: str, top_k=6, max_tokens=1000, temperature=0.2):
        # 1) Encode the query; ensure 2D shape (1, dim)
        q_emb = self.embeddings.encode([query], normalize=True, show_progress=False)
        if q_emb.ndim != 2 or q_emb.shape[0] != 1:
            # Defensive guard: make sure it is (1, dim)
            q_emb = q_emb.reshape(1, -1)

        # 2) Retrieve
        hits = self.vdb.search(q_emb, top_k=top_k)

        # 3) Build context from hits (handle empty results)
        if not hits:
            context = "No relevant context found in the indexed documents."
        else:
            context = "\n\n".join([f"[{h['rank']}] {h['text']}" for h in hits])

        # 4) Compose enhanced prompts
        system_prompt = """You are an expert Indian legal assistant with deep knowledge of Indian law. Your role is to provide accurate, well-structured, and professional legal information based strictly on the provided context.

RESPONSE GUIDELINES:
1. Structure your response with clear headings, subheadings, and numbered/bulleted lists
2. Use proper formatting with line breaks for readability
3. Cite specific sections, acts, and legal provisions when available
4. Provide comprehensive yet concise explanations
5. Use professional legal language while keeping it accessible
6. If information is incomplete, clearly state what cannot be found in the context

FORMATTING REQUIREMENTS:
- Use clear headings (##) for main sections
- Use subheadings (###) for subsections when needed
- Use numbered lists for sequential information
- Use bullet points for non-sequential information
- Bold important terms and legal provisions
- Separate different concepts with proper line spacing
- Always cite relevant legal sections and acts

IMPORTANT: Base your answer strictly on the provided context. If specific information is not available in the context, clearly state this limitation."""

        user_prompt = f"""Question: {query}

Please provide a comprehensive, well-structured answer based on the following legal context:

{context}

Ensure your response is professionally formatted, easy to read, and includes all relevant legal citations and sections mentioned in the context."""

        # 5) Call LLM with increased token limit for better responses
        completion = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        answer = completion.choices[0].message.content if completion.choices else ""
        return answer, hits
