from fastapi import APIRouter, UploadFile, File,Form
import os,shutil
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessageChunk, AIMessage
from app.graph.graph_builder import graph
from app.core.config import get_config
from app.rag.ingest import ingest_document
from app.rag.vectorstore import delete_vectorstore
from pydantic import BaseModel
import tempfile

class ChatRequest(BaseModel):
    query: str
    session_id: str

# # File Upload API
router= APIRouter()
@router.get("/")
def home():
    return {"message":"""FastAPI is working. add /docs path to test it. """}

from fastapi import APIRouter, UploadFile, File, Form
import tempfile
import os

router = APIRouter()

@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    old_session_id: str | None = Form(None)
):
    print("Received old_session_id:", old_session_id)

    # Delete previous vector store for this user/session
    if old_session_id:
        delete_vectorstore(old_session_id)

    suffix = os.path.splitext(file.filename)[1]

    temp_path = None

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            # to read the big files
            chunk = await file.read(1024 * 1024)

            while chunk:
                temp_file.write(chunk)
                chunk = await file.read(1024 * 1024)
 
            temp_path = temp_file.name

        # Ingest document
        result = ingest_document(temp_path)

        return {
            "message": "Upload successful",
            "session_id": result["session_id"],
            "chunks": result["chunks"]
        }

    finally:
        # Delete temporary file after ingestion
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

# Chat API with Streaming
@router.post("/chat")
async def chat(request: ChatRequest):

    query = request.query
    session_id = request.session_id

    async def event_generator():

        inputs = {
            "messages": [
                HumanMessage(content=query)
            ],
            "session_id":session_id
        }

        async for msg, metadata in graph.astream(
                    inputs,
                    config=get_config(session_id),
                    stream_mode="messages"
                ):
            # print(metadata)

            if metadata.get("langgraph_node") != "output_node":
                continue

            if isinstance(msg, (AIMessage, AIMessageChunk)):
                if msg.content:
                    yield msg.content

    return StreamingResponse(
        event_generator(),
        media_type="text/plain"
    )