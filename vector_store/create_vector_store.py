import faiss
import json
import os
from uuid import uuid4
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore

def create_vector_store():

    PATH_JSON = os.getenv("PATH_JSON")
    PATH_VECTOR_DISK = os.getenv("PATH_VECTOR_DISK")

    print("Iniciando criação da vector store ...")

    documentosFile = open(PATH_JSON, "r")
    documentos = json.loads(documentosFile.read())
    uuids = [str(uuid4()) for _ in documentos]

    for i in range(len(documentos)):
        documentos[i] = Document(page_content=documentos[i]["page_content"], metadata={"source": documentos[i]["metadata"]["source"], "enunciado": documentos[i]["metadata"]["enunciado"]})

    EMBEDDER = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    INDEXER = faiss.IndexFlatL2(len(EMBEDDER.embed_query("hello world")))

    vector_store = FAISS(
        embedding_function=EMBEDDER,
        index=INDEXER,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )

    remaining = len(documentos)
    tam_grupo = 100
    insercoes = 0
    offset = 0
    while remaining > 0:
        offset = insercoes * tam_grupo
        
        documentosInsercao = []
        uuidsInsercao = []
        
        for i in range(offset, offset + tam_grupo):
            if i >= len(documentos):
                break

            documentosInsercao.append(documentos[i])
            uuidsInsercao.append(uuids[i])
        
        print("Adicionando documentos n°{:d} - {:d} na memória ...".format(offset, offset + tam_grupo - 1))
        remaining -= tam_grupo + 1
        insercoes += 1

        vector_store.add_documents(documents=documentosInsercao, ids=uuidsInsercao) 
            
        
    vector_store.save_local(PATH_VECTOR_DISK)
    print("Vector store criada com sucesso...")

    return vector_store # FAISS