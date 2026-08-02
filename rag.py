import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("handbook")


def retrieve_context(question):
    # Create embedding for the question
    question_embedding = model.encode(question).tolist()

    # Search the vector database
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    # Check if anything was returned
    if not results["documents"] or not results["documents"][0]:
        return None, None

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("Distances:", distances)

    # Reject poor matches
    if distances[0] > 1.5:
        return None, None

    context = ""

    for doc in documents:
        context += doc + "\n\n"

    pages = sorted(set(meta["page"] for meta in metadatas))
    source = ", ".join(f"Page {page}" for page in pages)

    print("Retrieved Context:")
    print(context)

    return context, source