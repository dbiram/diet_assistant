import json
from pathlib import Path
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Load knowledge base
DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "knowledge_base.json"
with open(DATA_PATH, "r") as f:
    kb_texts = json.load(f)

# Prepare LangChain Documents
documents = [Document(page_content=text) for text in kb_texts]

# Load BGE embedding model
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

# Create FAISS vector store
vector_store = FAISS.from_documents(documents, embedding_model)

def personalize_query(profile: dict, question: str) -> str:
    profile_str = f"User Profile: {profile['gender']}, {profile['age']} years old, {profile['activity_level']} activity level."
    return profile_str + " " + question

def retrieve_top_k(profile: dict, question: str, k=3):
    personalized_query = personalize_query(profile, question)
    print(personalized_query)
    results = vector_store.similarity_search(personalized_query, k=k)
    return [doc.page_content for doc in results]
