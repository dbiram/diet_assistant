from app.rag.vector_store import (
    retrieve_dense_top_k,
    retrieve_sparse_top_k
)
from app.rag.generator import generate_text

def hybrid_retrieve_top_k(profile: dict, question: str, k=5):
    dense_results = retrieve_dense_top_k(profile, question, k=k)
    sparse_results = retrieve_sparse_top_k(profile, question, k=k)

    # Merge + deduplicate
    combined_results = list(set(dense_results + sparse_results))
    return combined_results[:k]

def generate_answer(profile: dict, question: str) -> str:
    # Retrieve relevant documents
    retrieved_docs = hybrid_retrieve_top_k(profile, question, k=3)
    context = "\n".join(retrieved_docs)

    # Build prompt
    prompt = (
        f"Here are relevant documents:\n{context}\n\n"
        f"User's profile:\n{profile}\n\n"
        f"Answer the user's question:\n{question}"
    )

    # Generate answer
    output = generate_text(prompt)
    answer = output.replace(prompt, "").strip()
    return answer
