# Builds and saves a FAISS vectorstore for later use.
# Converts the .txt files stored in the `data` directory into embeddings.
# The embeddings are stored in the `faiss_vectorstore` directory.

import os
import shutil
import dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

FAISS_DIR = "faiss_vectorstore"

dotenv.load_dotenv()
embedding_model = HuggingFaceInferenceAPIEmbeddings(api_key=os.getenv("HUGGINGFACE_API_KEY"),
                                  model_name="sentence-transformers/all-MiniLM-l6-v2")

data_loader = DirectoryLoader("data", glob="*.txt")
documents = data_loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
)
chunks = text_splitter.split_documents(documents)
vectorstore = FAISS.from_documents(chunks, embedding_model)

if os.path.exists(FAISS_DIR):
    shutil.rmtree(FAISS_DIR)
vectorstore.save_local(FAISS_DIR)