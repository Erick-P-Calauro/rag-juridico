from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def load_vector_store():
    PATH_VECTOR_DISK = "./data/Dvector_store"
    EMBEDDER = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(PATH_VECTOR_DISK, embeddings=EMBEDDER, allow_dangerous_deserialization=True)

    return vector_store