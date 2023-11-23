import os
from typing import Any

import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant


class MakeEmbeddings:
    def __init__(self, text, collection_name) -> None:
        self.text = text
        self.collection_name = collection_name

    @staticmethod
    def _chunk_docs(text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=50,
        )
        docs = [Document(page_content=x)
                for x in text_splitter.split_text(text)]
        return docs

    @staticmethod
    def _select_embedding_method(method):
        if method == 'HuggingFace':
            return HuggingFaceEmbeddings()
        elif method == 'OpenAI':
            return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_APIKEY'))

    def save_embeddings(self):
        Qdrant.from_documents(
            self.docs,
            self.embedding_model,
            url=os.getenv('QDRANT_HOST'),
            collection_name=self.collection_name,
        )

    def __call__(self) -> Any:

        self.docs = self._chunk_docs(self.text)

        method = st.selectbox('Select Embedding Method', ['OpenAI'])
        self.embedding_model = self._select_embedding_method(method)
