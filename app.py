# RAG Chatbot app
# Enter `streamlit run app_book_qa_only.py` in a terminal to run the app.

import os
import dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatCohere
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

dotenv.load_dotenv()


@st.cache_resource
def load_models():
    """Loads and caches the embedding and chat models in streamlit."""

    embedding_model = HuggingFaceInferenceAPIEmbeddings(api_key=os.getenv("HUGGINGFACE_API_KEY"))
    chat_model = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"))
    return embedding_model, chat_model


# Initialization
embedding_model, chat_model = load_models()
output_parser = StrOutputParser()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


@st.cache_resource
def load_vectorstore():
    """Loads a saved vectorstore and caches to streamlit."""

    vectorstore = FAISS.load_local("faiss_vectorstore",
                                   embedding_model,
                                   allow_dangerous_deserialization=True)
    return vectorstore


vectorstore = load_vectorstore()


def rag_chatbot(question):
    """Takes in a user's question, retrieves necessary context from a vectorstore,
    inputs the question and the context as a prompt into an LLM, and outputs the response."""

    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant who answers questions related to the book "The War of the Worlds".
    Do not answer other types of questions.
    Answer the question based only on the provided context.

    Context:
    {context}

    Question:
    {question}
    """)

    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",
                                         search_kwargs={"score_threshold": 0.2})
    qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | chat_model
            | output_parser
    )
    response = qa_chain.invoke(question)
    return response


# Streamlit
st.title("Book Q&A RAG Chatbot")

with st.container(height=113, border=True):
    st.write(""":green[This is a RAG Chatbot app that can answer questions related to the book "The War of the Worlds".
    The app cannot recognize the context from previous questions.
    So ensure that each question makes sense on its own.
    The Chatbot may sometimes hallucinate and give wrong answers.]""")

# Display messages
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Enter your question here")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    response = rag_chatbot(query)
    with st.chat_message("assistant"):
        st.markdown(response)

    # Log messages
    st.session_state["chat_history"].append({"role": "user", "content": query})
    st.session_state["chat_history"].append({"role": "assistant", "content": response})
