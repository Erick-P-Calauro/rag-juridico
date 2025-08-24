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
    N_CTX = int(os.getenv("CONTEXT_SIZE"))

    try:
        f = open(PATH_JSON, "r")
    except FileNotFoundError:
        scrapper()

    print("Iniciando conexão com LLM ...")
    print("Janela de contexto : {:d}".format(N_CTX))
    escolha_cpu_gpu = input("[0] - Iniciar modelo com GPU\n[1] - Iniciar modelo com CPU\nEntrada : ")

    try:
        if escolha_cpu_gpu == "0":
            print("Carregando modelo com a GPU ...")
            model = GPT4All(model_name=MODEL_NAME, allow_download=True, device="gpu", verbose=False, n_ctx=N_CTX)
        else:
            print("Carregando modelo com a CPU")
            model = GPT4All(model_name=MODEL_NAME, allow_download=True, device="cpu", verbose=False, n_ctx=N_CTX)
    
    except Exception:
        print("Carregamento falhou, mudando dispositivo ...")

        if escolha_cpu_gpu == "0":
            print("Carregando modelo com a CPU ...")
            model = GPT4All(model_name=MODEL_NAME, allow_download=True, device="cpu", verbose=False, n_ctx=N_CTX)
        else:
            print("Carregando modelo com a GPU")
            model = GPT4All(model_name=MODEL_NAME, allow_download=True, device="gpu", verbose=False, n_ctx=N_CTX)

    try:
        vector_store = load_vector_store()
    except Exception:
        print("Carregamento de vector store falhou ...")
        vector_store = create_vector_store()
    
    return [model, vector_store] # GPT4All, FAISS