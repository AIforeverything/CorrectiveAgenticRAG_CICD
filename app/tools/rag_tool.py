
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from app.rag.retriever import retrieve_docs
from app.graph.state import ChatState
from app.core.config import get_config

from langchain_core.runnables import RunnableConfig


@tool
def rag_tool(query: str, config: RunnableConfig) -> dict:
    """
    Retrieve relevant chunks from uploaded document.
    """

    session_id = config["configurable"]["thread_id"]

    docs = retrieve_docs(
        query=query,
        session_id=session_id
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # print("Data from rag_tool: ",context)
    return {
        "filtered_context": context
    }