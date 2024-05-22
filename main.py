import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time

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
        if chat["role"] == "assistant" and "response_time" in chat:
            st.write(f"<sub><i>Response time: {chat['response_time']}</i></sub>", unsafe_allow_html=True)

prompt = st.chat_input("Paste any article for summarising")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "message":prompt})
    start_time = time.time()
    response = requests.post(url, json={'query': prompt})
    end_time = time.time()
    response_duration_formatted = f"{end_time-start_time:.2f} seconds"
    output = response.json()['result']
    response_text = output["response_text"]
    with st.chat_message("assistant"):
        st.markdown(response_text)
        st.write(f"<sub><i>Response time: {response_duration_formatted}</i></sub>", unsafe_allow_html=True)
    st.session_state.messages.append({"role":"assistant", "message":response_text, "response_time": response_duration_formatted})
    