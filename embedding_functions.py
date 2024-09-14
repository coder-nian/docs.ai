import os
from dotenv import load_dotenv
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings import JinaEmbeddings

load_dotenv()


def embedding_api():
    return JinaEmbeddings(jina_api_key=os.getenv("JINA_API_KEY"), model_name="jina-embeddings-v2-base-en")


def embedding_llm():
    return OllamaEmbeddings(model="nomic-embed-text")
