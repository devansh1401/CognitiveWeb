# from .utils import WebBaseLoader, RecursiveCharacterTextSplitter, Chroma, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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