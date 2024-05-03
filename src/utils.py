from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq

def get_vectorstore_from_urls(urls):
    document_chunks = []
    for url in urls:
        if url:
            loader = WebBaseLoader(url)
            document = loader.load()
            text_splitter = RecursiveCharacterTextSplitter()
            document_chunks.extend(text_splitter.split_documents(document))

    if document_chunks:
        vector_store = Chroma.from_documents(document_chunks, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
        return vector_store
    else:
        return None

def get_context_retriever_chain(vector_store):
    llm = ChatGroq(model="mixtral-8x7b-32768")

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    llm = ChatGroq(model="mixtral-8x7b-32768")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

def get_response(user_input, vector_store):
    retriever_chain = get_context_retriever_chain(vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    chat_history = [(role, message) for role, message in st.session_state.chat_history]

    response = conversation_rag_chain.invoke({
        "chat_history": chat_history,
        "input": user_input
    })

    return response['answer']