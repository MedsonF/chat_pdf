from pathlib import Path
import os

import streamlit as st
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI

from docling import DoclingConverter

from dotenv import load_dotenv

from configs import *

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


PASTA_ARQUIVOS = Path(__file__).parent / 'arquivos'


def importacao_documentos():
    documentos = []
    converter = DoclingConverter()  # Inicializa o conversor do Docling

    # Lista de extensões de arquivo suportadas
    extensoes = ['*.pdf', '*.xlsx']

    for extensao in extensoes:
        for arquivo in Path("PASTA_ARQUIVOS").glob(extensao):
            # Converte o arquivo para Markdown e JSON
            resultado = converter.convert(arquivo)
            markdown = resultado.document.export_to_markdown()

            # Adiciona os resultados à lista de documentos
            documentos.append({
                "arquivo": arquivo.name,
                "markdown": markdown
            })

    return documentos

def split_de_documentos(documentos):
    recur_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        separators=["/n\n", "\n", ".", " ", ""]
    )
    documentos = recur_splitter.split_documents(documentos)

    for i, doc in enumerate(documentos):
        doc.metadata['source'] = doc.metadata['source'].split('/')[-1]
        doc.metadata['doc_id'] = i
    return documentos

def cria_vector_store(documentos):
    embedding_model = OpenAIEmbeddings(openai_api_key=api_key)
    vector_store = FAISS.from_documents(
        documents=documentos,
        embedding=embedding_model
    )
    return vector_store

def cria_chain_conversa():

    documentos = importacao_documentos()
    documentos = split_de_documentos(documentos)
    vector_store = cria_vector_store(documentos)

    chat = ChatOpenAI(model=get_config('model_name'))
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key='chat_history',
        output_key='answer'
        )
    retriever = vector_store.as_retriever(
        search_type=get_config('retrieval_search_type'),
        search_kwargs=get_config('retrieval_kwargs')
    )
    prompt = PromptTemplate.from_template(get_config('prompt'))
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={'prompt': prompt}
    )

    st.session_state['chain'] = chat_chain
