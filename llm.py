import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(context, question):
    prompt = f"""
You are an AI assistant answering questions from a student handbook.

IMPORTANT RULES:
- Use ONLY the handbook context.
- Do NOT summarize unless the user asks for a summary.
- Include ALL relevant details from the handbook.
- If the answer is not found in the handbook, reply exactly:
I don't know.

HANDBOOK CONTEXT:
{context}

QUESTION:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content