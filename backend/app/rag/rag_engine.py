from app.rag.vector_store import (
    retrieve_dense_top_k,
    retrieve_sparse_top_k,
    personalize_query
)
from app.rag.reranker import rerank
from app.rag.generator import generate_text
from app.auth.models import User
from sqlalchemy.orm import Session

def split_into_subqueries(question: str) -> list:
    """
    Naive multi-hop question splitter.
    """
    if " and " in question.lower():
        parts = question.lower().split(" and ")
        return [part.strip().capitalize() for part in parts]
    else:
        return [question]

def multi_hop_retrieve_with_rerank(profile: dict, question: str, initial_k=20, rerank_top_k=3):
    subqueries = split_into_subqueries(question)
    all_passages = []
    for subquery in subqueries:
        # Run dense and sparse retrieval (both profile-aware)
        dense_results = retrieve_dense_top_k(profile, subquery, k=initial_k)
        sparse_results = retrieve_sparse_top_k(profile, subquery, k=initial_k)

        # Merge + deduplicate
        combined_results = list(set(dense_results + sparse_results))
        all_passages.extend(combined_results)

    # Deduplicate all results from sub-queries
    all_passages = list(set(all_passages))
    # Rerank merged passages using profile-aware query
    personalized_query = personalize_query(profile, question)
    final_passages = rerank(personalized_query, all_passages, top_k=rerank_top_k)
    if len(final_passages) == 0:
        # Self-check fallback: retry without profile grounding
        print("⚠️ No documents found — retrying without profile grounding...")
        dense_results = retrieve_dense_top_k(profile, question, k=initial_k)
        sparse_results = retrieve_sparse_top_k(profile, question, k=initial_k)
        fallback_results = list(set(dense_results + sparse_results))
        final_passages = fallback_results[:rerank_top_k]

    return final_passages

def generate_answer(profile: dict, question: str, user: User, db: Session) -> str:
    # Retrieve relevant documents
    retrieved_docs = multi_hop_retrieve_with_rerank(profile, question, initial_k=30, rerank_top_k=5)
    context = "\n".join(retrieved_docs)

    # Build prompt
    prompt = (
        f"Here are relevant documents:\n{context}\n\n"
        f"User's profile:\n{profile}\n\n"
        f"Answer the user's question:\n{question}"
    )
    print(f"Generated prompt:\n{prompt}\n")
    output = generate_text(prompt, user_id=user.id, db=db, max_length=512)
    answer = output.replace(prompt, "").strip()
    result = answer.replace("Answer:", "").strip()
    return result
