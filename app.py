import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with SlayBot!",  # Keep emoji in the title
    page_icon=":brain:",  # Use emoji as page icon
    layout="centered",
)

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Set up Google Gemini-Pro AI model
default_model = 'gemini-pro'


# Sidebar for settings
st.sidebar.header("Settings")
selected_model = st.sidebar.selectbox("Select Model", options=["gemini-pro", "gemini-lite"], index=0)

# Initialize the selected model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel(selected_model)

# Function to translate roles between Streamlit and Gemini-Pro
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Main chat title
st.title("Gemini - SlayBot💅")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# User input field
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

# Sidebar options for saving or resetting chat
st.sidebar.header("Actions")
if st.sidebar.button("Download Chat History"):
    history = "\n".join(
        [f"{translate_role_for_streamlit(m.role).capitalize()}: {m.parts[0].text}" for m in st.session_state.chat_session.history]
    )
    st.sidebar.download_button("Download", history, file_name="chat_history.txt")

if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.experimental_rerun()
