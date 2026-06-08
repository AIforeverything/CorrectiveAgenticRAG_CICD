from app.rag.vectorstore import get_retriever

def retrieve_docs(query: str,session_id: str):
    retriever = get_retriever(session_id)
    retrieved=retriever.invoke(query)
    # print(retrieved)
    return retrieved