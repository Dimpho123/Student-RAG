import pickle
import chromadb

# Load TF-IDF vectorizer
with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("handbook")


questions = [
    "What are the live class times?",
    "What happens after the first 12 weeks?"
]


for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    question_embedding = vectorizer.transform(
        [question]
    ).toarray()[0].tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1
    ):

        print(f"\nRESULT {i}")
        print("Distance:", distance)
        print("Source:", metadata)
        print("Text:")
        print(document[:500])