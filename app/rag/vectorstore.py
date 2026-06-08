from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import shutil

# Local embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    encode_kwargs={"normalize_embeddings": True}
)

VECTORSTORE_DIR = "vectorstores"

def get_faiss_path(session_id: str) -> str:
    return os.path.join(VECTORSTORE_DIR, session_id)

def create_vectorstore(documents, session_id):

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    vectorstore = FAISS.from_documents(
        documents,
        embeddings
    )
    
    vectorstore.save_local(
        f"{VECTORSTORE_DIR}/{session_id}"
    )

def load_vectorstore(session_id: str):

    faiss_path = get_faiss_path(session_id)

    if not os.path.exists(faiss_path):
        raise FileNotFoundError(
            f"No vectorstore found for session_id = {session_id}"
        )

    return FAISS.load_local(
        faiss_path,
        embeddings,
        allow_dangerous_deserialization=True
    )


def get_retriever(session_id):

    vectorstore = FAISS.load_local(
        f"vectorstores/{session_id}",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever()

def delete_vectorstore(session_id: str):
    faiss_path = get_faiss_path(session_id)
    print("Exists:", os.path.exists(faiss_path))
    print("Deleting:", faiss_path)
    
    if os.path.exists(faiss_path):
        shutil.rmtree(faiss_path)