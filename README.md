# RAG-Chatbot

This ia a RAG Chatbot app that can answer various questions. It retrieves the necessary information from Wikipedia.

### How to run the app
To run the hosted Streamlit app, go to this link: https://llm-rag-chatbot.streamlit.app/

To run the Streamlit app locally, follow these instructions:

1. Install Python - You need a python 3.x installation.
2. Clone The Repository - Open a terminal/command prompt and navigate to the directory where you want to store the application. Then, run `git clone https://github.com/odil-T/RAG-Chatbot.git` to clone the repository.
3. Make A New Environment - Navigate into the cloned repository directory with `cd RAG-Chatbot` and run `pip install virtualenv`. Run `virtualenv chat_app` to make a new virtual environment. Run `chat_app\Scripts\activate` in Windows or `source chat_app/bin/activate` in Mac/Linux to activate the environment.
5. Install Dependencies - While the virtual environment is active, install the required libraries by running `pip install -r requirements.txt`.
6. Get API Key - Make an account in https://cohere.com/ and get your Cohere API key.
7. Save API Key - To let the app access the API key, you will need to make a new file in your working directory called `.env`. Open the file and write `COHERE_API_KEY=`. Enter your API key after the `=` sign without leaving spaces. Save the file.
8. Run The App - You can launch the application by running `streamlit run app.py`. This launches the Streamlit app locally. A new window should appear in your browser.
9. You can close the app by closing the terminal/command prompt. If you wish to reopen it, open the terminal/command prompt in `RAG-Chatbot` directory and run `chat_app\Scripts\activate`, followed by `streamlit run app.py`. 
