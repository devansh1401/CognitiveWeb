#from .utils import ChatGroq, MessagesPlaceholder, ChatPromptTemplate, create_history_aware_retriever
from langchain_groq import ChatGroq
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain.chains import create_history_aware_retriever
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