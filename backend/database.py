import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["customer_support_ai"]
conversations = db["conversations"]


def save_message(session_id: str, sender: str, message: str, intent: str = None):
    """Saves a single chat message to MongoDB."""
    doc = {
        "session_id": session_id,
        "sender": sender,  # "user" or "bot"
        "message": message,
        "intent": intent,
        "timestamp": datetime.utcnow(),
    }
    conversations.insert_one(doc)


def get_conversation_history(session_id: str):
    """Retrieves all messages for a given session, sorted by time."""
    messages = conversations.find({"session_id": session_id}).sort("timestamp", 1)
    return [
        {
            "sender": m["sender"],
            "message": m["message"],
            "intent": m.get("intent"),
            "timestamp": m["timestamp"].isoformat(),
        }
        for m in messages
    ]