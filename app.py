from fastapi import FastAPI
from pydantic import BaseModel

from rag import retrieve_context
from llm import generate_answer

app = FastAPI(title="Student Handbook RAG API")


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(data: Question):

    # Empty question
    if not data.question.strip():
        return {
            "error": "Question cannot be empty."
        }

    try:
        context, source = retrieve_context(data.question)

        if context is None:
            return {
                "answer": "I don't know.",
                "source": None
            }

        answer = generate_answer(context, data.question)

        return {
            "answer": answer,
            "source": source
        }

    except Exception as e:
        return {
            "error": str(e)
        }