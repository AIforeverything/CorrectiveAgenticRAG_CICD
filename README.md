LangSmith graph, the backend architecture of your **Corrective Agentic RAG (CRAG)** project can be represented as:

                    ┌─────────────────┐
                    │ User Query      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ chatbot         │
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
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ output_node     │
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
 ├── chatbot (GROQ)
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
 │     └── (GROQ)
 │
 └── output_node
       └── (GROQ)
 │
 ▼
Streamlit Frontend

Observability & Evaluation:
LangSmith

CI/CD:
GitHub → GitHub Actions → AWS Free Tier

