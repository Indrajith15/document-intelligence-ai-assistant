import os 
from dotenv import load_dotenv
from google import genai
import chromadb
from pathlib import Path
import uuid 

load_dotenv()

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(
    dotenv_path=PROJECT_ROOT / ".env",
    override=True
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API Key not found")

client = genai.Client(api_key=api_key)

def generate_embedding(text):
    result = client.models.embed_content(
        model = "gemini-embedding-001",
        contents = text
    )
    return result.embeddings[0].values




# Create a persistent ChromaDB client
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

# Create or access our collection
collection = chroma_client.get_or_create_collection(
    name="document_chunks",
    metadata={"hnsw:space": "cosine"}
)


def store_chunks(chunks):
    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        chunk_id = str(uuid.uuid4())

        ids.append(chunk_id)
        documents.append(chunk["text"])
        embeddings.append(
            generate_embedding(chunk["text"])
        )
        metadatas.append(chunk["metadata"])

    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    return len(ids)



def retrieve_relevant_chunks(question, top_k=3):

    # Generate an embedding for the user's question
    question_embedding = generate_embedding(question)

    # Check whether the database contains documents
    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    # Search ChromaDB for similar embeddings
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, total_chunks),
        include=["documents", "metadatas", "distances"]
    )

    # Organize the retrieved results
    retrieved_chunks = []

    for i, document in enumerate(results["documents"][0]):
        retrieved_chunks.append({
            "text": document,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved_chunks


def generate_answer(question, retrieved_chunks):

    # Combine the retrieved chunks into one context
    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    # Create the prompt for Gemini
    prompt = f"""
    You are a helpful document question-answering assistant.

    Answer the user's question using ONLY the information
    provided in the context below.

    If the answer is not available in the context,
    clearly say that the uploaded document does not contain
    enough information to answer.

    Context:
    {context}

    User's Question:
    {question}

    Answer:
    """

    # Send the prompt to Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text


