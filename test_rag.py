from rag import retrieve_context

context, source = retrieve_context("What is the attendance requirement?")

print("SOURCE:", source)
print()
print(context)