import os
from dotenv import load_dotenv
from gpt4all import GPT4All
from vector_store.load_vector_store import load_vector_store
from vector_store.create_vector_store import create_vector_store
from data.scrapper import scrapper

def setup():
    load_dotenv()

    PATH_JSON = os.getenv("PATH_JSON")
    MODEL_NAME = os.getenv("LLM_MODEL_NAME") 

    try:
        f = open(PATH_JSON, "r")
    except FileNotFoundError:
        scrapper()

    print("Iniciando conexão com LLM ...")
    model = GPT4All(model_name=MODEL_NAME, allow_download=True, device="gpu", verbose=False, n_ctx=4096)

    try:
        vector_store = load_vector_store()
    except Exception:
        print("Carregamento de vector store falhou ...")
        vector_store = create_vector_store()
    
    return [model, vector_store] # GPT4All, FAISS