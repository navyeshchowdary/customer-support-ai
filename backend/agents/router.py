from agents.llm import client, MODEL_NAME, generate_response
from agents.billing import handle_billing_query
from agents.technical import handle_technical_query
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rag"))
from vector_store import search_knowledge_base

INTENT_PROMPT = """You are an intent classifier for a customer support system.
Classify the customer's message into exactly ONE of these categories:
- billing (payments, refunds, invoices, subscriptions)
- technical (product issues, troubleshooting, login problems)
- general (shipping, warranty, account/login, FAQs, greetings, complaints, anything else)

Respond with ONLY the single word: billing, technical, or general. No explanation.

Customer message: {query}
"""

GENERAL_SYSTEM_PROMPT = """You are a friendly Customer Support Agent for TechMart Electronics.
Answer questions about shipping, warranty, general policies, or anything not billing/technical-specific.
Be warm, concise, and helpful."""


def detect_intent(user_query: str) -> str:
    prompt = INTENT_PROMPT.format(query=user_query)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    intent = response.text.strip().lower()

    if "billing" in intent:
        return "billing"
    elif "technical" in intent:
        return "technical"
    else:
        return "general"


def handle_general_query(user_query: str) -> str:
    context_chunks = search_knowledge_base(user_query, k=3)
    context = "\n\n".join(context_chunks)
    return generate_response(GENERAL_SYSTEM_PROMPT, context, user_query)


def route_query(user_query: str) -> dict:
    """Detects intent and routes the query to the correct agent."""
    intent = detect_intent(user_query)

    if intent == "billing":
        response = handle_billing_query(user_query)
    elif intent == "technical":
        response = handle_technical_query(user_query)
    else:
        response = handle_general_query(user_query)

    return {"intent": intent, "response": response}