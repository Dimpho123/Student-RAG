import pickle

import chromadb



# Load the TF-IDF vectorizer


with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)



# Connect to ChromaDB


client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "handbook"
)



# Retrieve relevant context


def retrieve_context(question):

    # Convert question into an embedding
    question_embedding = vectorizer.transform(
        [question]
    ).toarray()[0].tolist()


    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=10
    )


    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]


    if not documents:
        return None, None


   
    # Check whether the query has any useful vocabulary
    

    if not any(question_embedding):
        return None, None


 
    # Course questions
    

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


        compare_documents = compare_results.get(
            "documents",
            []
        )

        compare_metadatas = compare_results.get(
            "metadatas",
            []
        )


        for document, metadata in zip(
            compare_documents[:5],
            compare_metadatas[:5]
        ):

            if document not in documents:

                documents.append(document)
                metadatas.append(metadata)


 
    # Build context
    

    context_parts = []

    sources = []


    for document, metadata in zip(
        documents,
        metadatas
    ):

        source_type = metadata.get(
            "source"
        )


        if source_type == "Handbook":

            page = metadata.get(
                "page"
            )


            context_parts.append(
                f"Source: Student Handbook - Page {page}\n"
                f"{document}"
            )


            source = (
                f"Student Handbook - Page {page}"
            )


            if source not in sources:

                sources.append(source)


        elif source_type == "Website":

            url = metadata.get(
                "url"
            )


            context_parts.append(
                f"Source: ZAIO Website - {url}\n"
                f"{document}"
            )


            source = (
                f"ZAIO Website - {url}"
            )


            if source not in sources:

                sources.append(source)


    context = "\n\n".join(
        context_parts
    )


    return context, sources