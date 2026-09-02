import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("handbook")


def retrieve_context(question):
    # Convert the question into an embedding
    question_embedding = model.encode(question).tolist()

    # Search across BOTH the handbook and website
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=10
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        return None, None

    # Check whether the best retrieved result is relevant enough
    if distances[0] > 1.5:
        return None, None

    # ---------------------------------------------------------
    # If the question is about courses/programmes,
    # also retrieve the ZAIO course comparison page.
    # ---------------------------------------------------------

    question_lower = question.lower()

    course_keywords = [
        "course",
        "courses",
        "programme",
        "programmes",
        "program",
        "programs",
        "qualification",
        "qualifications",
        "what can i study",
        "what does zaio offer"
    ]

    is_course_question = any(
        keyword in question_lower
        for keyword in course_keywords
    )

    if is_course_question:

        compare_results = collection.get(
            where={
                "url": "https://www.zaio.io/compare-courses"
            }
        )

        compare_documents = compare_results.get("documents", [])
        compare_metadatas = compare_results.get("metadatas", [])

        # Add the comparison page content to the retrieved results
        for document, metadata in zip(
            compare_documents[:5],
            compare_metadatas[:5]
        ):

            if document not in documents:
                documents.append(document)
                metadatas.append(metadata)

    # ---------------------------------------------------------
    # Build the final context and source list
    # ---------------------------------------------------------

    context_parts = []
    sources = []

    for document, metadata in zip(documents, metadatas):

        source_type = metadata.get("source")

        if source_type == "Handbook":

            page = metadata.get("page")

            context_parts.append(
                f"Source: Student Handbook - Page {page}\n"
                f"{document}"
            )

            source = f"Student Handbook - Page {page}"

            if source not in sources:
                sources.append(source)

        elif source_type == "Website":

            url = metadata.get("url")

            context_parts.append(
                f"Source: ZAIO Website - {url}\n"
                f"{document}"
            )

            source = f"ZAIO Website - {url}"

            if source not in sources:
                sources.append(source)

    context = "\n\n".join(context_parts)

    return context, sources