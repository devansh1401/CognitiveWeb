# from .utils import ChatGroq, MessagesPlaceholder, ChatPromptTemplate, create_stuff_documents_chain, create_retrieval_chain
from langchain_groq import ChatGroq
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
def get_conversational_rag_chain(retriever_chain):
    llm = ChatGroq(model="mixtral-8x7b-32768")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)