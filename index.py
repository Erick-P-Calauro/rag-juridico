from gpt4all import GPT4All
from load_vector_store import load_vector_store
from create_vector_store import create_vector_store

print("Iniciando RAG ...")
MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf" 
model = GPT4All(model_name=MODEL_NAME, allow_download=True, device="gpu", verbose=False)

print("Carregando banco de vetors...")
vector_store = load_vector_store()

# Hyde (Documento Hipotético)
entrada = input("Entrada : \n")

print("Gerando Hyde ...")
hyde = model.generate(entrada, max_tokens=256, temp=0.7)
contexto_docs = vector_store.similarity_search(hyde, k=3)

print("Injetando contexto ...")
contexto = ""
for d in contexto_docs:
    contexto += d.metadata.get("source")
    contexto += "\n"
    contexto += d.metadata.get("enunciado")
    contexto += "\n"
    contexto += d.page_content
    contexto += "\n\n"

print(contexto)

saida = ""
with model.chat_session(system_prompt="Responda com base no CONTEXTO a seguir : \n" + contexto):
    saida = model.generate(entrada, max_tokens=1024, temp=0.2)

print("Resposta do modelo : \n" + saida)