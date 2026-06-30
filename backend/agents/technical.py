import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rag"))
from vector_store import search_knowledge_base
from agents.llm import generate_response

SYSTEM_PROMPT = """You are a Technical Support Agent for TechMart Electronics. 
You specialize in product issues, troubleshooting, login problems, and technical errors. 
Be clear, step-by-step, and patient."""


def handle_technical_query(user_query: str) -> str:
    context_chunks = search_knowledge_base(user_query, k=3)
    context = "\n\n".join(context_chunks)
    return generate_response(SYSTEM_PROMPT, context, user_query)