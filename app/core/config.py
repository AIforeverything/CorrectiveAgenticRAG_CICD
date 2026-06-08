import uuid

def get_config(session_id: str):
    return {
        "configurable": {
            "thread_id": session_id
        },
        "metadata": {
            "id": str(uuid.uuid4())
        },
        "run_name": "chat"
    }