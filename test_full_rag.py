from rag import retrieve_context
from llm import generate_answer


questions = [
    "What are the live class times?",
    "How do I join classes?",
    "What courses does ZAIO offer?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("=" * 60)

    # Step 1: Retrieve relevant information
    context, sources = retrieve_context(question)

    print("\nDEBUG - CONTEXT FOUND:", context is not None)
    print("DEBUG - SOURCES FOUND:", sources)

    if context is None:
        print("\nANSWER: I don't know.")
        continue

    # Step 2: Generate an answer using the retrieved context
    answer = generate_answer(context, question)

    print("\nANSWER:")
    print(answer)

    print("\nSOURCES:")
    if sources:
        for source in sources:
            print("-", source)
    else:
        print("NO SOURCES FOUND")