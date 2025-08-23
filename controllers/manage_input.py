# Tipos de entrada : GPT4All, FAISS, String

SYSPROMPT = """
    "Você é um assistende de uma área jurídica. 
    Busque desenvolver as bases jurídicas necessárias. 
    Se não houver certeza, diga que não sabe. 
    Responda com base no CONTEXTO a seguir : \n"
"""

def manage_input(model, vector_store, entrada):
    contexto_docs = vector_store.similarity_search(entrada, k=3)

    contexto = ""
    for d in contexto_docs:
        contexto += d.metadata.get("source") + "\n"
        contexto += d.metadata.get("enunciado") + "\n"
        contexto += d.page_content + "\n\n"

    print("Gerando Resposta ...")
    saida = ""
    with model.chat_session(system_prompt=SYSPROMPT + contexto):
        saida = model.generate(entrada, max_tokens=1024, temp=0.2)

    return saida # String