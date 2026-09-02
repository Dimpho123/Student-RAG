import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("handbook")

results = collection.get(
    include=["metadatas"]
)

handbook_count = 0
website_count = 0
missing_source = 0

for metadata in results["metadatas"]:

    source = metadata.get("source")

    if source == "Website":
        website_count += 1

    elif source == "Handbook":
        handbook_count += 1

    else:
        missing_source += 1


print("Handbook chunks:", handbook_count)
print("Website chunks:", website_count)
print("Missing source:", missing_source)
print("Total chunks:", len(results["metadatas"]))