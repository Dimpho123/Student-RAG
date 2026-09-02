from rag import retrieve_context

questions = [
    "What are the live class times?",
    "How do I join classes?",
    "What courses does ZAIO offer?"
]

for question in questions:
    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("=" * 60)

    context, source = retrieve_context(question)

    if context is None:
        print("NO RELEVANT INFORMATION FOUND")
    else:
        print("SOURCE:", source)
        print("\nCONTEXT:")
        print(context[:3000])