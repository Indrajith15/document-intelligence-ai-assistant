
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from io import BytesIO

from backend.document_processor import process_document

from backend.rag import (
    store_chunks,
    retrieve_relevant_chunks,
    generate_answer
)


app = FastAPI()

# Maximum PDF upload size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024


@app.get("/")
def home():
    return {
        "message": "Welcome to document Intelligence AI"
    }


# Request model for the chat endpoint
class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(request: QuestionRequest):

    # Validate the question
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty."
        )

    # Retrieve relevant chunks from ChromaDB
    retrieved_chunks = retrieve_relevant_chunks(
        question,
        top_k=3
    )

    # Check whether any relevant chunks were found
    if not retrieved_chunks:
        return {
            "question": question,
            "answer": "No documents found. Please upload a PDF first."
        }

    # Generate an answer using Gemini
    answer = generate_answer(
        question,
        retrieved_chunks
    )

    return {
        "question": question,
        "answer": answer,
        "source_chunks": retrieved_chunks
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Document Intelligence API is running!"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Validate filename
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=415,
            detail="Only PDF files are allowed."
        )

    # Read uploaded file
    file_content = await file.read()

    # Validate empty file
    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    # Validate file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 10 MB limit."
        )

    # Validate actual PDF file signature
    if not file_content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=415,
            detail="The uploaded file is not a valid PDF."
        )

    # Read PDF content
    try:
        pdf_reader = PdfReader(BytesIO(file_content))

        # Check whether PDF is password protected
        if pdf_reader.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="Password-protected PDFs are not supported."
            )

        total_pages = len(pdf_reader.pages)

    except PdfReadError:
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF is corrupted or invalid."
        )

    # Process PDF into chunks
    processed_chunks = process_document(
        pdf_reader,
        file.filename
    )

    # Check whether text was extracted
    if not processed_chunks:
        raise HTTPException(
            status_code=400,
            detail="No extractable text found in the PDF."
        )

    # Store embeddings and chunks in ChromaDB
    total_stored = store_chunks(processed_chunks)

    return {
        "filename": file.filename,
        "total_pages": total_pages,
        "total_chunks": len(processed_chunks),
        "total_stored": total_stored
    }
