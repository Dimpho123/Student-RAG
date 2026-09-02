import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(context, question):
    prompt = f"""
You are an AI assistant answering questions using trusted ZAIO information.

IMPORTANT RULES:
- Use ONLY the information provided in the retrieved context.
- The context may come from the Student Handbook or the official ZAIO website.
- Do NOT use outside knowledge.
- Do NOT make up or assume information that is not contained in the context.
- Answer the question directly and clearly.
- Include all relevant details from the retrieved context.
- If the answer cannot be found in the retrieved context, reply exactly:
I don't know.If the answer cannot be found in the retrieved context, reply exactly:
I could not find that information in the available knowledge base.

HANDBOOK CONTEXT:
{context}

QUESTION:
{question}

Answer:
"""

    response = client.chat.completions.create(
       model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content