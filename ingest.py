import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Open the handbook
doc = fitz.open("handbook.pdf")

# Extract text from every page
documents = []

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text()

    if text.strip():
        documents.append({
            "text": text,
            "page": page_num + 1
        })

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = []

for document in documents:
    split_text = splitter.split_text(document["text"])

    for chunk in split_text:
        chunks.append({
            "text": chunk,
            "page": document["page"]
        })

print(f"Created {len(chunks)} handbook chunks")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("handbook")

# Store handbook embeddings
for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk["text"]).tolist()

    collection.upsert(
        ids=[f"handbook_{i}"],
        embeddings=[embedding],
        documents=[chunk["text"]],
        metadatas=[{
            "source": "Handbook",
            "page": chunk["page"]
        }]
    )

print(f"Stored {len(chunks)} handbook chunks in ChromaDB")