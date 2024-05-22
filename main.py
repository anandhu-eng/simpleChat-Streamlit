import streamlit as st
import requests
from dotenv import load_dotenv
import os

#load the env variable from .env file 
load_dotenv()
url = os.getenv('URL')

# the messages should be of format {"role":"user/assistant","message":"prompt/response"}
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.chat_message("assistant"):
    st.write("Hello 👋\n Im a summarisation bot!\n I will be happy to summarise any article😇")

for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.write(chat["message"])

prompt = st.chat_input("Paste any article for summarising")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "message":prompt})
    response = requests.post(url, json={'query': prompt})
    output = response.json()['result']
    response_text = output["response_text"]
    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.session_state.messages.append({"role":"assistant", "message":response_text})
    