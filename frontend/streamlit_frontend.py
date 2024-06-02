import streamlit as st
import requests

PRODUCTION_URL="https://chatcv-production.up.railway.app/invoke"
DEVELOPMENT_URL="http://0.0.0.0:8000/invoke"

if PRODUCTION_URL:
    URL = PRODUCTION_URL
else:
    URL = DEVELOPMENT_URL

# Set page configuration for a wide layout
st.set_page_config(page_title="Chatbot CV Lorenzo Baraldi", layout="wide")

# Custom CSS for styling the chat interface
st.markdown("""
    <style>
    .chat-message {
        max-width: 70%;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 16px;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #dcf8c6;
        align-self: flex-end;
        color: black;
    }
    .bot-message {
        background-color: #f1f0f0;
        align-self: flex-start;
        color: black;
    }
    .message-container {
        display: flex;
        flex-direction: column;
    }
    .chat-container {
        display: flex;
        flex-direction: column-reverse;
        max-height: 70vh;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fff;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Chatbot Interface")

# Initialize session state for messages and chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get response from the FastAPI service
def get_response(question, chat_history):
    url = URL
    inputs = {"input": {"question": question, "chat_history": chat_history}}
    print(inputs)
    response = requests.post(url, json=inputs)
    return response.json()["output"]

# Template questions for quick access
template_questions = [
    "Tell me about Lorenzo Baraldi.",
    "What are Lorenzo's research field?",
    "What are Lorenzo's publications? Provide the link.",
]

# Sidebar with quick questions
with st.sidebar:
    st.header("Quick Questions")
    for question in template_questions:
        if st.button(question):
            response = get_response(question, st.session_state.chat_history)
            st.session_state.messages.append(("You", question))
            st.session_state.messages.append(("Bot", response))
            st.session_state.chat_history.append((question, response))

# Main chat container
chat_container = st.container()
with chat_container:
    st.header("Chat")
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, message in reversed(st.session_state.messages):  # Reverse the order of messages
        if sender == "You":
            st.markdown(f'<div class="chat-message user-message"><b>{sender}:</b> {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message"><b>{sender}:</b> {message}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Chat form for user input
with st.form(key="chat_form"):
    user_input = st.text_area("You:", height=100)
    submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        response = get_response(user_input, st.session_state.chat_history)
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("Bot", response))
        st.session_state.chat_history.append((user_input, response))
        st.experimental_rerun()

