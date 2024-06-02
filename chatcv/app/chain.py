import os
import sys
import getpass
import bs4
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
import dotenv
from llama_index.core import SimpleDirectoryReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder


from operator import itemgetter
from typing import List, Tuple

from fastapi import FastAPI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, format_document
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field
from app.prompts import DEFAULT_DOCUMENT_PROMPT, CONDENSE_QUESTION_PROMPT, ANSWER_PROMPT
ROOT = os.path.dirname((os.path.dirname(__file__)))
# Load the OpenAI API and LangChain key from the environment
dotenv.load_dotenv()
# User input

class ChatHistory(BaseModel):
    """Chat history with the bot."""

    chat_history: List[Tuple[str, str]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "question"}},
    )
    question: str

def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    """Combine documents into a single string."""
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

def _format_chat_history(chat_history: List[Tuple]) -> str:
    """Format chat history into a string."""
    buffer = ""
    for dialogue_turn in chat_history:
        human = "Human: " + dialogue_turn[0]
        ai = "Assistant: " + dialogue_turn[1]
        buffer += "\n" + "\n".join([human, ai])
    return buffer

def calculate_embeddings_rag():
    '''
        Calculate embeddings for rag, open folder media and recalculate all embeddings
    '''
    reader = SimpleDirectoryReader(
        input_dir=os.path.join(ROOT,"media"),
        recursive=True
    )
    docs = reader.load_data()
    print(f"Loaded {len(docs)} docs")
    documents = [doc.to_langchain_format() for doc in docs]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")
    

def get_chain():
    '''
        Get the chain for the app
    '''
    vectorstore=Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
    if len(vectorstore.get()['ids']) == 0:
        calculate_embeddings_rag()
        vectorstore=Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    _inputs = RunnableMap(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: _format_chat_history(x["chat_history"])
        )
        | CONDENSE_QUESTION_PROMPT
        | ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
        | StrOutputParser(),
    )

    _context = {
        "context": itemgetter("standalone_question") | retriever | _combine_documents,
        "question": lambda x: x["standalone_question"],
    }
    conversational_qa_chain = (
        _inputs | _context | ANSWER_PROMPT | ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0) | StrOutputParser()
    )
    chain = conversational_qa_chain.with_types(input_type=ChatHistory)
    return chain

    # response = rag_chain.invoke({"input": "Who is Lorenzo Baraldi?"})
    # response["answer"]
if __name__ == "__main__":
    get_chain()