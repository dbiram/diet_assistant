from app.rag.vector_store import retrieve_top_k
from app.rag.generator import generate_text

def generate_answer(profile: dict, question: str) -> str:
    # Retrieve relevant documents
    retrieved_docs = retrieve_top_k(profile, question, k=3)
    context = "\n".join(retrieved_docs)

    # Build prompt
    prompt = (
        f"Here are relevant documents:\n{context}\n\n"
        f"Answer the user's question:\n{question}"
    )

    # Generate answer
    output = generate_text(prompt)
    answer = output.replace(prompt, "").strip()
    return answer
