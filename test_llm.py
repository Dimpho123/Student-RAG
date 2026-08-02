from llm import generate_answer

context = """
Students are required to attend at least 80% of their classes.
"""

question = "What is the attendance requirement?"

answer = generate_answer(context, question)

print(answer)