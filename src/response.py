import streamlit as st
from vectorstore import get_vectorstore_from_urls
from retriever_chain import get_context_retriever_chain
from conversational_rag_chain import get_conversational_rag_chain
from langchain_core.messages import AIMessage, HumanMessage

def get_response(user_input, vector_store):
    retriever_chain = get_context_retriever_chain(vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    chat_history = [
        AIMessage(content=message) if role == "AI" else HumanMessage(content=message)
        for role, message in st.session_state.chat_history
    ]

    response = conversation_rag_chain.invoke({
        "chat_history": chat_history,
        "input": user_input
    })

    return response['answer']