# Student Handbook RAG Assistant

## Overview

This project is a Retrieval-Augmented Generation (RAG) system built with Python.

The assistant answers questions using a student handbook PDF.

If the answer cannot be found in the handbook, it responds:

"I don't know."

---

## Technologies

- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- Groq API
- LangChain
- PyPDF

---

## Features

- Loads a PDF handbook
- Extracts text
- Splits text into chunks
- Creates embeddings
- Stores embeddings in ChromaDB
- Retrieves relevant handbook sections
- Uses an LLM to answer questions
- Returns the handbook page number
- REST API
- Ready for n8n integration

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Build the Database

```bash
python ingest.py
```

---

## Run the API

```bash
uvicorn app:app --reload
```

---

## API Endpoint

POST

```
/ask
```

Example

```json
{
  "question": "What are the hardware requirements?"
}
```

Response

```json
{
  "answer": "...",
  "source": "Page 5"
}
```

---

## Run Tests

```bash
pytest
```