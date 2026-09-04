# Student RAG Assistant

## Overview

The Student RAG Assistant is a Retrieval-Augmented Generation (RAG) system built with Python and FastAPI.

The assistant answers student questions using information retrieved from two knowledge sources:

* ZAIO Student Handbook PDF
* ZAIO website

The system retrieves relevant information from the knowledge base before generating an answer. If the required information cannot be found, the assistant refuses to answer instead of generating unsupported information.

The project is also integrated with n8n for workflow automation and Discord for presenting responses to users.

---

## Technologies

* Python
* FastAPI
* ChromaDB
* Scikit-learn
* Groq API
* LangChain Text Splitters
* PyMuPDF
* BeautifulSoup4
* Playwright
* pytest
* n8n
* Discord Webhooks

---

## Features

* Loads and processes the Student Handbook PDF
* Extracts and cleans ZAIO website content
* Crawls multiple ZAIO website pages
* Splits documents into smaller chunks
* Generates embeddings for the knowledge sources
* Stores embeddings in ChromaDB
* Searches across the Student Handbook and ZAIO website
* Retrieves relevant context for user questions
* Generates answers using the retrieved context
* Returns the source used to answer the question
* Refuses questions when information is not available
* Provides a FastAPI `/ask` endpoint
* Supports n8n workflow integration
* Sends responses to Discord
* Includes automated API/unit tests

---

## Knowledge Sources

### Student Handbook

The Student Handbook is processed from a PDF document.

Metadata includes:

* Source
* PDF page number

### ZAIO Website

The ZAIO website is crawled and processed using Playwright and BeautifulSoup.

Metadata includes:

* Source
* Website URL
* Page information

Both sources are stored in the same ChromaDB collection.

---

## RAG Pipeline

The system follows this process:

```text
User Question
      ↓
Question Embedding
      ↓
ChromaDB Similarity Search
      ↓
Retrieve Relevant Chunks
      ↓
Generate Answer Using Retrieved Context
      ↓
Return Answer + Source
```

If relevant information cannot be found in the knowledge base, the assistant responds:

```text
I could not find that information in the available knowledge base.
```

---

## Installation

Clone the repository and enter the project directory:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Student-rag
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
playwright install
```

---

## Environment Variables

Create a `.env` file in the project directory and add the required Groq API key:

```text
GROQ_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

---

## Build the Knowledge Base

To process the Student Handbook:

```bash
python ingest.py
```

To crawl and process the ZAIO website:

```bash
python ingest_website.py
```

The processed information is stored in ChromaDB.

---

## Run the API

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

---

## API Endpoint

### POST `/ask`

The endpoint accepts a student question.

Example request:

```json
{
  "question": "What are the live class times?"
}
```

Example response:

```json
{
  "answer": "Live classes are scheduled as follows...",
  "source": "Student Handbook - Page 11"
}
```

For questions that cannot be answered from the knowledge base:

```json
{
  "answer": "I could not find that information in the available knowledge base.",
  "source": null
}
```

---

## n8n Integration

The RAG API is connected to an n8n workflow.

The workflow follows:

```text
Webhook
   ↓
HTTP Request
   ↓
RAG API
   ↓
Discord
   ↓
Respond to Webhook
```

The n8n workflow accepts a student's question, sends it to the RAG API, receives the generated answer and source, and forwards the response to Discord.

---

## Testing

The project includes automated API/unit tests using pytest.

Run all tests with:

```bash
pytest -v
```

The current test suite contains 9 tests covering:

* Student Handbook questions
* ZAIO website questions
* Unanswerable questions

Current result:

```text
9 passed
```

Detailed test results are documented in:

```text
test_results.md
```

---

## Project Structure

```text
Student-rag/
│
├── app.py
├── rag.py
├── llm.py
├── ingest.py
├── ingest_website.py
├── crawl_zaio.py
├── requirements.txt
├── README.md
├── test_api.py
├── test_results.md
├── handbook.pdf
├── vectorizer.pkl
├── chroma_db/
│
├── tests/
│
└── .gitignore
```

---

## Test Categories

The assistant was tested using three categories:

1. **Student Handbook**

   * Live class times
   * How to join classes
   * What happens after the first 12 weeks

2. **ZAIO Website**

   * Courses offered by ZAIO
   * Available bootcamps
   * Online learning information

3. **Unanswerable Questions**

   * Population of South Africa
   * Weather information
   * Latest football results

All 9 tests passed successfully.

---

## Project Goal

The goal of this project is to demonstrate how Retrieval-Augmented Generation can be used to create a reliable student information assistant that retrieves information from approved knowledge sources and avoids generating answers when the required information is unavailable.
