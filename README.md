Based on your LangSmith graph, the backend architecture of your **Corrective Agentic RAG (CRAG)** project can be represented as:

                    ┌─────────────────┐
                    │ User Query      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ chatbot         │
                    │ Llama-3.3-70B   │
                    │ (Reasoning)     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ tools_condition │
                    └────────┬────────┘
                             │
               ┌─────────────┴─────────────┐
               │ Need Knowledge?           │
               └─────────────┬─────────────┘
                             │ Yes
                             ▼
                    ┌─────────────────┐
                    │ rag_tool        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ VectorStore     │
                    │ Retriever       │
                    │ (FAISS +        │
                    │ Embeddings)     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ knowledge_      │
                    │ filtering       │
                    │ Llama-3.1-8B    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ output_node     │
                    │ Llama-3.1-8B    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Final Response  │
                    └─────────────────┘
### Backend Tech Stack

User
 │
 ▼
FastAPI
 │
 ▼
LangGraph Workflow
 │
 ├── chatbot (Llama-3.3-70B via GROQ)
 │
 ├── Tool Calling
 │     │
 │     └── rag_tool
 │             │
 │             ├── HuggingFace Embeddings
 │             ├── FAISS Vector Store
 │             └── Retriever
 │
 ├── knowledge_filtering
 │     └── Llama-3.1-8B
 │
 └── output_node
       └── Llama-3.1-8B
 │
 ▼
Streamlit Frontend

Observability & Evaluation:
LangSmith

CI/CD:
GitHub → GitHub Actions → AWS Free Tier

