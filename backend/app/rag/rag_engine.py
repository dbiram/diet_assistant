from app.rag.vector_store import (
    retrieve_dense_top_k,
    retrieve_sparse_top_k,
    personalize_query
)
from app.rag.reranker import rerank
from app.rag.generator import generate_text

def hybrid_retrieve_with_rerank(profile: dict, question: str, initial_k=20, rerank_top_k=3):
    # Run dense and sparse retrieval (both profile-aware)
    dense_results = retrieve_dense_top_k(profile, question, k=initial_k)
    sparse_results = retrieve_sparse_top_k(profile, question, k=initial_k)

    # Merge + deduplicate
    combined_results = list(set(dense_results + sparse_results))

    # Rerank merged passages using profile-aware query
    personalized_query = personalize_query(profile, question)
    final_passages = rerank(personalized_query, combined_results, top_k=rerank_top_k)

    return final_passages

def generate_answer(profile: dict, question: str) -> str:
    # Retrieve relevant documents
    retrieved_docs = hybrid_retrieve_with_rerank(profile, question)
    context = "\n".join(retrieved_docs)

    print(f"Retrieved context:\n{context}\n")

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
