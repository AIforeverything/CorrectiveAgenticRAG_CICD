import uuid
import time
from langchain_community.document_loaders import (
    TextLoader,
    Docx2txtLoader,
    PyMuPDFLoader,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.vectorstore import create_vectorstore

def ingest_document(file_path: str):
    
    start= time.perf_counter()
    session_id = str(uuid.uuid4())

    if file_path.lower().endswith(".pdf"):
        loader= PyMuPDFLoader(file_path)

    elif file_path.lower().endswith(".txt"):
        loader = TextLoader(file_path)

    elif file_path.lower().endswith(".docx"):
        loader = Docx2txtLoader(file_path)

    else:
        raise ValueError(
            "Supported formats: .pdf, .txt, .docx"
        )

    docs = loader.load()
    print(f"Loading time: {time.perf_counter()-start:.2f} s")

    split_time=time.perf_counter()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)
    print(f"Splitting+Chunking:{time.perf_counter()-split_time:.2f} s")

    vs_start = time.perf_counter()

    create_vectorstore(
        documents=chunks,
        session_id=session_id
    )

    print(f"Embeddings + FAISS: {time.perf_counter()-vs_start:.2f}s")

    print(f"Execution Total time: {time.perf_counter()-start :.2f} seconds")

    return {
        "session_id": session_id,
        "chunks": len(chunks)
    }