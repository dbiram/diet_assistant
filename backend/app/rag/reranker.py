from sentence_transformers import CrossEncoder

# Load reranker model once globally
reranker_model = CrossEncoder('BAAI/bge-reranker-base') 

def rerank(query: str, passages: list, top_k=3):
    """
    Rerank passages given a query and return top_k most relevant.
    """
    # Prepare input pairs: (query, passage)
    pairs = [(query, passage) for passage in passages]

    # Get relevance scores
    scores = reranker_model.predict(pairs)

    # Sort passages by descending score
    ranked_passages = sorted(zip(scores, passages), key=lambda x: x[0], reverse=True)

    # Return top_k passages
    return [passage for score, passage in ranked_passages[:top_k]]
