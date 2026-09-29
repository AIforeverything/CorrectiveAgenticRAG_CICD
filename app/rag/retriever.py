from app.rag.vectorstore import get_retriever
from sentence_transformers import CrossEncoder

# Load reranker once when application starts
reranker = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L2-v2")


def retrieve_docs(query: str, session_id: str):

    # Step 1: FAISS retrieves top 10 candidates
    retriever = get_retriever(session_id)
    retrieved_docs = retriever.invoke(query)

    if not retrieved_docs:
        return []

    # Step 2: Create query-document pairs
    pairs = [[query, doc.page_content] for doc in retrieved_docs]

    # Step 3: Calculate reranking scores
    scores = reranker.predict(pairs)

    # Step 4: Attach scores to documents
    scored_docs = list(zip(retrieved_docs, scores))

    # Step 5: Sort by reranker score
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # Step 6: Keep top 3
    reranked_docs = [doc for doc, score in scored_docs[:3]]

    return reranked_docs
