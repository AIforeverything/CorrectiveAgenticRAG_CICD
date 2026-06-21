from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)
from langgraph.prebuilt import ToolNode

from app.core.llm import llm
from app.core.llm import llm2
from app.tools.rag_tool import rag_tool
from app.graph.state import ChatState
from app.rag.retriever import retrieve_docs
import json


tools = [rag_tool]

llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)

def chatbot_node(state: ChatState)->dict:

    SYSTEM_PROMPT = """
    You are a RAG assistant.

    Answer ONLY from retrieved context.

    If context contains no relevent information in the given document uploaded by the user then reply exactly:
    "Sorry, the given document doesn't contain the information for the question."

    Do not hallucinate.
    """
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ]

    # preserving the ORIGINAL AIMessage object
    response = llm_with_tools.invoke(messages)

    # returning full response object
    return {
        "messages": [response]
    }

def knowledge_filtering(state: ChatState):

    query = next(
                msg.content
                for msg in reversed(state["messages"])
                if isinstance(msg, HumanMessage)
            )
    # print("Query1 : \n",query)
    tool_message = next(
            msg for msg in reversed(state["messages"])
            if isinstance(msg, ToolMessage)
        )
    tool_data = json.loads(tool_message.content)
    context = tool_data["filtered_context"]
    # print("context before knowledge filtering in knowledge filtering : \n",context)

    SYSTEM_PROMPT = f"""
    if the {context} is "Sorry, the given document doesn't contain the information for the question.":
        return the "Sorry, the given document doesn't contain the information for the question." 
        to next node directly and do not process.

    else the {context} is not "Sorry, the given document doesn't contain the information for the question.":
        Check each sentence in the context and determine whether it is relevant
        to answer the query.

        Query:
        {query}

        Context:
        {context}

        Remove irrelevant sentences.
        Combine relevant sentences into a single paragraph and return the paragraph as context.

    use this node only once and do not loop through it.
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        context
    ]

    response = llm2.invoke(messages)

    filtered_context = response.content
    # print("filtered context after knowledge Filtering: \n",filtered_context)

    return {
        "filtered_context": filtered_context
    }

def output_node(state:ChatState)->dict:

    query = next(
                msg.content
                for msg in reversed(state["messages"])
                if isinstance(msg, HumanMessage)
            )

    filtered_context=state['filtered_context']

    SYSTEM_PROMPT = f"""
                    If the {filtered_context} is "Sorry, the given document doesn't contain the information for the question.":
                        return the "Sorry, the given document doesn't contain the information for the question." 
                        to next node directly and do not process.

                    else the {filtered_context} is not "Sorry, the given document doesn't contain the information for the question.":
                        You are a RAG assistant.

                        Answer the user's question using ONLY the supplied context.

                        Do not repeat or summarize the entire context.
                        Provide only the answer.

                        If the answer is not present in the context, return exactly:
                        Sorry, the given document doesn't contain the information for the question.

                        Do not hallucinate.
                    """
    
    messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=f"""
                            Question:
                            {query}
                            Context:
                            {filtered_context}
                            """)
                ]
    if filtered_context == "Sorry, the given document doesn't contain the information for the question.":
        return {
            "messages": [
                AIMessage(
                    content="Sorry, the given document doesn't contain the information for the question."
                )
            ]
        }

    response = llm2.invoke(messages)

    # print("QUERY:", query)
    # print("FILTERED_CONTEXT:", filtered_context[:500])
    # print("FINAL_ANSWER:", response.content)

    return {
        "messages": [response]
    }