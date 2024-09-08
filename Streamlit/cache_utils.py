import streamlit as st
from datetime import datetime  
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
import os, ollama
from config import (EMBED_MODEL,
                    STARTING_PROMPT_PATH,
                    SYSTEM_PROMPT_PATH,
                    OLLAMA_HOST,
                    QDRANT_HOST)

@st.cache_resource
def load_prompts():
    with open(SYSTEM_PROMPT_PATH, 'r') as file:
        system_prompt = file.read()

    with open(STARTING_PROMPT_PATH, 'r') as file:
        starting_prompt = file.read()

    # Insert the current datetime into the system prompt
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_prompt = system_prompt.replace("{current_datetime}", current_datetime)
    return system_prompt, starting_prompt

@st.cache_resource(ttl=300)
def init_ollama_client():
    return ollama.Client(host=OLLAMA_HOST)

@st.cache_resource(ttl=300)
def init_qdrant_client():
    return QdrantClient(host=QDRANT_HOST, grpc_port=6334, prefer_grpc=True)

@st.cache_resource
def init_embed_model():
    return TextEmbedding(model_name=EMBED_MODEL)
