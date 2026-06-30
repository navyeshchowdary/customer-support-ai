import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"


def generate_response(system_prompt: str, context: str, user_query: str) -> str:
    """Combines a system prompt, retrieved context, and the user's question to get an LLM answer."""

    full_prompt = f"""{system_prompt}

Here is relevant information from our knowledge base:
{context}

Customer question: {user_query}

Answer the customer's question clearly and helpfully using the information above. 
If the knowledge base doesn't contain the answer, politely say you'll escalate it to a human agent.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt,
    )
    return response.text