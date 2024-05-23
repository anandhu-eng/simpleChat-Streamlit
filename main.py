import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time
from streamlit_option_menu import option_menu
import json
from random import sample
import threading
from queue import Queue


selected = option_menu(
    menu_title=None, 
    options=["Chat", "Benchmark"], 
    icons=['chat-dots', 'cpu', ], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal")




#load the env variable from .env file 
load_dotenv()
url = os.getenv('URL')

def is_url_reachable(url, query):
    print(query)
    try:
        response = requests.post(url, json={'query': query})
        return response.status_code == 200
    except requests.RequestException as e:
        return False

if selected == "Chat":
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

if selected == "Benchmark":
    # specifiying the number of samples and the json file from which data is to be taken
    noOfSamples = st.text_input("Enter the number of samples the QPS should be tested for")
    json_file = st.file_uploader("Upload JSON file", type=["json"])
    # Custom CSS for the circular button
    st.markdown("""
        <style>
        .circular-button {
            display: inline-block;
            border-radius: 50%;
            background-color: #4CAF50;
            color: white;
            padding: 20px 40px;
            font-size: 24px;
            text-align: center;
            cursor: pointer;
            margin: 10px;
        }
        .circular-button:active {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False          

    # To identify whether any error occured
    errorFlag = 0

    def client_predict_worker(query):
        """Serialize the query, send it to the server, and return the deserialized response."""
        try:
            response = requests.post(url, json={'query': query})
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
            global errorFlag
            errorFlag = 1
            

     # Function to simulate progress
    def run_benchmark():
        if not noOfSamples:
            st.error('Number of samples is not specified or it is not an integer!', icon="🚨") 
            return -1
        if not json_file:
            st.error('JSON file is not specified!', icon="🚨") 
            return -1
        
        max_num_threads = os.cpu_count()
        num_samples = int(noOfSamples)
        data = json.load(json_file)

        if num_samples > len(data):
            st.error('Number of samples exceeds the data available in the JSON file!', icon="🚨")
            return -1
        
        selected_samples = sample(data, num_samples)
        

        if not is_url_reachable(url, selected_samples[0]["input"]):
            st.error('URL is not reachable!', icon="🚨") 
            return -1   
        else:
            st.success('Server is reachable!', icon="✅")

        progress_bar = st.progress(0)
        threads = []

        start_time = time.time()
        for i,sample_data in enumerate(selected_samples):
            query = sample_data['input']
            while threading.active_count() >= max_num_threads:
                time.sleep(0.0001)
            thread = threading.Thread(target=client_predict_worker, args=(query,))
            thread.start()
            threads.append(thread)
            progress_bar.progress((i+1)/int(noOfSamples))

        for thread in threads:
            thread.join()

        end_time = time.time()

        avg_response_time = (end_time-start_time) / int(noOfSamples)

        st.write(f"QPS for {num_samples} samples: {avg_response_time:.2f} seconds")
        return avg_response_time

    if not st.session_state.button_clicked:
        if st.button("GO!", key="go_button"):
            st.session_state.button_clicked = True
            response = run_benchmark()  # Run the benchmark and show progress
            if response:
                if errorFlag:
                    st.error('There was some server error in between!', icon="🚨") 
                else:
                    st.success("Recording QPS successfull without any Errors!", icon="✅")
   