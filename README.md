# 📄 Document Intelligence AI Assistant

An AI-powered document question-answering application that allows users to upload PDF documents and ask questions about their content. Built using **Retrieval-Augmented Generation (RAG)**, the application retrieves relevant information from uploaded documents and generates context-grounded answers using Google's Gemini models.

## 🚀 Project Overview

The Document Intelligence AI Assistant simplifies information extraction from PDF documents.

Instead of manually searching through lengthy documents, users can upload a PDF and interact with its contents through a conversational interface.

The application uses a RAG pipeline to retrieve relevant document chunks and generate answers based on the uploaded content, reducing unsupported responses.

## ✨ Features

- **PDF Upload:** Upload PDF documents through an interactive interface.
- **Text Extraction:** Extract text from PDF documents using PyPDF.
- **Document Chunking:** Split extracted text into smaller, manageable chunks using LangChain.
- **Text Embeddings:** Generate vector embeddings using Google's Gemini Embedding model.
- **Vector Storage:** Store document embeddings and metadata in ChromaDB.
- **Semantic Search:** Retrieve relevant document chunks based on user questions.
- **AI-Powered Responses:** Generate context-grounded answers using Gemini.
- **Conversational Interface:** Interact with documents through a Streamlit chat interface.
- **Input Validation:** Validate uploaded PDFs, file size, and user questions.
- **Error Handling:** Handle backend connection failures and request timeouts.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | Gemini Embedding 001 |
| Vector Database | ChromaDB |
| Document Processing | PyPDF |
| Text Chunking | LangChain |
| API Communication | REST API, HTTP, JSON |
| Configuration | Python-dotenv |

## 🏗️ Architecture

The application follows a Retrieval-Augmented Generation (RAG) architecture.

### Document Processing Pipeline

1. User uploads a PDF through Streamlit.
2. FastAPI receives the uploaded document.
3. PyPDF extracts the document text.
4. LangChain splits the text into smaller chunks.
5. Gemini generates embeddings for each chunk.
6. ChromaDB stores the embeddings and metadata.

### Question Answering Pipeline

1. User submits a question through the chat interface.
2. Streamlit sends the question to the FastAPI backend.
3. Gemini generates an embedding for the question.
4. ChromaDB retrieves the most relevant document chunks.
5. Retrieved context is passed to Gemini 2.5 Flash.
6. Gemini generates an answer using the retrieved document content.
7. The answer is displayed in the Streamlit interface.

## 📂 Project Structure

```text
Document_Intelligence_AI/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── rag.py
│   └── document_processor.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── uploads/
│
├── chroma_db/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

**Note:** The `.env`, `.venv`, and local ChromaDB data are excluded from GitHub.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Indrajith15/document-intelligence-ai-assistant.git

cd document-intelligence-ai-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Important:** Never commit your `.env` file or expose your API key publicly.

## ▶️ Running the Application

The application requires two terminals.

### Terminal 1: Start the FastAPI backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

Backend URL:

```text
