from fastapi import FastAPI
from pydantic import BaseModel

from rag import retrieve_context
from llm import generate_answer


# Create the FastAPI application
app = FastAPI(
    title="ZAIO RAG Assistant API",
    description="API for answering questions using the ZAIO Student Handbook and website.",
    version="1.0.0"
)


# Request format
class QuestionRequest(BaseModel):
    question: str


# Response format
class QuestionResponse(BaseModel):
    answer: str
    source: str | None


def choose_source(question, sources):
    """
    Choose the most appropriate source for the question.
    """

    if not sources:
        return None

    question_lower = question.lower()

    # Questions specifically about live classes, joining classes,
    # bootcamp rules, or student procedures are usually answered
    # by the Student Handbook.
    handbook_keywords = [
        "live class",
        "live classes",
        "join classes",
        "joining classes",
        "google classroom",
        "zoom",
        "tutor",
        "discord",
        "bootcamp schedule",
        "schedule",
        "first 12 weeks"
    ]

    for keyword in handbook_keywords:
        if keyword in question_lower:

            for source in sources:
                if source.startswith("Student Handbook"):
                    return source

    # Questions about courses/programmes are better represented
    # by ZAIO's course comparison page when it is available.
    course_keywords = [
        "what courses",
        "which courses",
        "courses does zaio offer",
        "programmes",
        "programs",
        "qualifications",
        "what can i study"
    ]

    for keyword in course_keywords:
        if keyword in question_lower:

            for source in sources:
                if "compare-courses" in source:
                    return source

    # Otherwise use the highest-ranked retrieved source.
    return sources[0]


@app.get("/")
def home():
    return {
        "message": "ZAIO RAG Assistant API is running"
    }


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    # Retrieve relevant information from ChromaDB
    context, sources = retrieve_context(request.question)

    # If no relevant information was found
    if context is None:
        return QuestionResponse(
            answer="I could not find that information in the available knowledge base.",
            source=None
        )

    # Generate an answer using ONLY the retrieved context
    answer = generate_answer(context, request.question)

    # If the assistant could not find the answer,
    # do not return a source.
    if answer.strip() == "I could not find that information in the available knowledge base.":

        source = None

    else:

        source = choose_source(
            request.question,
            sources
        )

    return QuestionResponse(
        answer=answer,
        source=source
    )