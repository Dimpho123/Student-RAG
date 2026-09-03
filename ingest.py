import os
import pickle

import chromadb
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.feature_extraction.text import TfidfVectorizer



# Connect to ChromaDB


client = chromadb.PersistentClient(path="chroma_db")


# Delete the old collection if it exists
try:
    client.delete_collection("handbook")
except Exception:
    pass


# Create a fresh collection
collection = client.create_collection("handbook")



# Load the Student Handbook PDF


pdf = fitz.open("handbook.pdf")



# Text splitter


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)


documents = []
metadatas = []
ids = []



# Extract and split handbook pages


for page_number, page in enumerate(pdf, start=1):

    text = page.get_text()

    if not text.strip():
        continue

    chunks = text_splitter.split_text(text)

    for chunk_number, chunk in enumerate(chunks):

        documents.append(chunk)

        metadatas.append({
            "source": "Handbook",
            "page": page_number
        })

        ids.append(
            f"handbook-{page_number}-{chunk_number}"
        )



# Create TF-IDF embeddings


vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

embeddings = vectorizer.fit_transform(documents).toarray()



# Save the vectorizer


with open("vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)



# Store embeddings in ChromaDB


collection.add(
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas,
    ids=ids
)


print(
    f"Successfully added {len(documents)} handbook chunks to ChromaDB."
)

print("TF-IDF vectorizer saved as vectorizer.pkl")