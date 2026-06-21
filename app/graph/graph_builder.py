from langgraph.graph import START, StateGraph, END

from app.graph.state import ChatState
from app.graph.nodes import chatbot_node,tool_node,knowledge_filtering,output_node

from langgraph.prebuilt.tool_node import tools_condition
from langgraph.checkpoint.memory import InMemorySaver

# state
graph_builder= StateGraph(ChatState) 

graph_builder.add_node("chatbot",chatbot_node)
graph_builder.add_node("tools",tool_node)
graph_builder.add_node("knowledge_filtering", knowledge_filtering)
graph_builder.add_node("output_node",output_node)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",tools_condition)
graph_builder.add_edge("tools","knowledge_filtering")
graph_builder.add_edge("knowledge_filtering","output_node")
graph_builder.add_edge("output_node",END)

# memory=InMemorySaver()

# graph=graph_builder.compile(checkpointer=memory)
graph= graph_builder.compile()


