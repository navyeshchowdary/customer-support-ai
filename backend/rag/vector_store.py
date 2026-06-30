import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Path to our knowledge base file
KNOWLEDGE_BASE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "knowledge_base", "sample_policy.txt"
)

VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")


def build_vector_store():
    """Loads the knowledge base, splits it into chunks, embeds it, and saves a FAISS index."""

    # 1. Load the document
    loader = TextLoader(KNOWLEDGE_BASE_PATH, encoding="utf-8")
    documents = loader.load()

    # 2. Split into smaller chunks so retrieval is precise
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)

    # 3. Create embeddings (turns text into vectors) using a free local model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Build the FAISS vector store and save it locally
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)

    print(f"Vector store built successfully with {len(chunks)} chunks.")
    return vector_store


def load_vector_store():
    """Loads an existing FAISS index from disk."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True
    )
    return vector_store


def search_knowledge_base(query: str, k: int = 3):
    """Searches the vector store and returns the top-k most relevant chunks."""
    vector_store = load_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]


# Run this file directly to build the index for the first time
if __name__ == "__main__":
    build_vector_store()