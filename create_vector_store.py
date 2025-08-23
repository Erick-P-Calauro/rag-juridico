import faiss
import json
from uuid import uuid4
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore

PATH_JSON =  "./data/documentos.json"
PATH_VECTOR_DISK = "./data/Dvector_store"

def create_vector_store():
    documentosFile = open(PATH_JSON, "r")
    documentos = json.loads(documentosFile.read())
    uuids = [str(uuid4()) for _ in documentos]

    for i in range(len(documentos)):
        documentos[i] = Document(page_content=documentos[i]["page_content"], metadata={"source": documentos[i]["metadata"]["source"], "enunciado": documentos[i]["metadata"]["enunciado"]})

        print("Documentos convertidos.")

        EMBEDDER = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        INDEXER = faiss.IndexFlatL2(len(EMBEDDER.embed_query("hello world")))

        vector_store = FAISS(
            embedding_function=EMBEDDER,
            index=INDEXER,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )

        print("Banco vetorial criado.")

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
            
            print("Adicionando {:d} - {:d} na memória ...".format(offset, offset + tam_grupo - 1))
            remaining -= tam_grupo + 1
            insercoes += 1

            vector_store.add_documents(documents=documentosInsercao, ids=uuidsInsercao) 
            
        
        print("Documentos na memória.")
        vector_store.save_local(PATH_VECTOR_DISK)
        print("Documentos armazenados em disco.")