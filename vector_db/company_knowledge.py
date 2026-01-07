import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# ✅ LOAD ENV FIRST
load_dotenv()

client = OpenAI()

CHROMA_PATH = "vector_db_store"
COLLECTION_NAME = "company_knowledge"

def get_collection():
    chroma_client = chromadb.Client(
        chromadb.config.Settings(
            persist_directory=CHROMA_PATH
        )
    )
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )

def embed_text(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def load_company_docs(folder_path: str):
    collection = get_collection()

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            embedding = embed_text(content)

            collection.add(
                documents=[content],
                embeddings=[embedding],
                ids=[filename]
            )

    print("✅ Company knowledge loaded into Vector DB")

def query_company_knowledge(query: str, top_k: int = 3):
    collection = get_collection()
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]
