from config import GOOGLE_API_KEY, GROQ_API_KEY
import streamlit as st
import google.generativeai as genai
from utils import AIMessage, HumanMessage
from vectorstore import get_vectorstore_from_urls
from response import get_response

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# App config
st.set_page_config(page_title="CognitiveWeb", page_icon="🕸️", layout="wide")

# Header
st.title("CognitiveWeb 🤖")
st.write("Explore and chat with websites like never before!")

# Sidebar
with st.sidebar:
    st.header("Settings")
    website_url1 = st.text_input("Website URL 1")
    website_url2 = st.text_input("Website URL 2")
    website_url3 = st.text_input("Website URL 3")

    st.divider()
    st.write("**About CognitiveWeb**")
    st.write("CognitiveWeb is an AI-powered tool that allows you to explore and chat with websites, extracting relevant information to answer your queries.")
    st.write("Created with ❤️ by [Devansh](https://twitter.com/devansh_1405)")

# Get the list of URLs that have been entered
website_urls = [website_url1, website_url2, website_url3]

if "vector_store" not in st.session_state or any(url for url in website_urls if url):
    # Create the vector store if it doesn't exist or if any of the URLs have changed
    st.session_state.vector_store = get_vectorstore_from_urls(website_urls)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("AI", "Hello, I am a bot. How can I help you?"),
    ]

# User input
with st.container():
    user_query = st.text_area("Type your message here...", height=100)
    if user_query is not None and user_query != "":
        if st.session_state.vector_store:
            response = get_response(user_query, st.session_state.vector_store)
            st.session_state.chat_history.append(("Human", user_query))
            st.session_state.chat_history.append(("AI", response))
        else:
            st.info("Please enter at least one website URL to get started.")

# Conversation
with st.container():
    st.subheader("Conversation")
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

# Footer
with st.container():
    st.write("---")
    st.markdown(
        f'<div style="text-align:center;">Powered by <a href="https://grok.ai" target="_blank">Grok AI</a> and <a href="https://gemini.google.com" target="_blank">Google Gemini</a></div>',
        unsafe_allow_html=True
    )