from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid

from agents.router import route_query
from database import save_message, get_conversation_history
from rag.vector_store import build_vector_store, VECTOR_STORE_PATH

load_dotenv()

app = FastAPI(title="Customer Support AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    if not os.path.exists(VECTOR_STORE_PATH):
        print("Vector store not found. Building it now...")
        build_vector_store()
        print("Vector store built successfully.")
    else:
        print("Vector store already exists.")


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.get("/")
def read_root():
    return {"message": "Customer Support AI backend is running!"}


@app.get("/health")
def health_check():
    api_key_loaded = bool(os.getenv("GOOGLE_API_KEY"))
    return {"status": "ok", "api_key_loaded": api_key_loaded}


@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    save_message(session_id, "user", request.message)

    result = route_query(request.message)

    save_message(session_id, "bot", result["response"], intent=result["intent"])

    return {
        "intent": result["intent"],
        "response": result["response"],
        "session_id": session_id,
    }


@app.get("/history/{session_id}")
def get_history(session_id: str):
    return {"session_id": session_id, "messages": get_conversation_history(session_id)}