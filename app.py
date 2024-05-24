# RAG Chatbot app
# Enter `streamlit run app.py` in a terminal to run the app.

import os
import dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import WikipediaRetriever
from langchain_cohere import ChatCohere

dotenv.load_dotenv()


@st.cache_resource
def load_model():
    """Loads and caches the chat model in streamlit."""

    chat_model = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"))
    return chat_model


# Initialization
retriever = WikipediaRetriever()
chat_model = load_model()
output_parser = StrOutputParser()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def rag_chatbot(question):
    """Takes in a user's question, retrieves necessary context from Wikipedia,
    inputs the question and the context as a prompt into an LLM, and outputs the response."""

    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the provided context.
    Do not answer inappropriate questions.

    Context:
    {context}

    Question:
    {question}
    """)

    qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | chat_model
            | output_parser
    )
    response = qa_chain.invoke(question)
    return response


# Streamlit
st.title("Wikipedia Q&A RAG Chatbot")

with st.container(height=113, border=True):
    st.write(""":green[This is a RAG Chatbot app that can answer various questions. 
    It uses Wikipedia to retrieve relevant information.
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
