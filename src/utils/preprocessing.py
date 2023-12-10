import os
from typing import Any

import docker
import pandas as pd
import streamlit as st
from langchain.embeddings import (
    HuggingFaceEmbeddings, OllamaEmbeddings,
    OpenAIEmbeddings,
)
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant
from sqlalchemy import create_engine

from utils.conf_loaders import load_config

embeddings_providers = load_config(custom_key='embeddings').keys()
embeddings_models = load_config(custom_key='embeddings')


class MakeEmbeddings:
    def __init__(self, text, collection_name) -> None:
        self.text = text
        self.collection_name = collection_name

    def _embedding_model_params(self):
        self.chunk_size = st.number_input('Chunk Size', 0, 1000, 100)
        self.chunk_overlap = st.slider('Chunk Overlap', 0, 1000, 50)

    @staticmethod
    def _chunk_docs(text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=50,
        )
        docs = [
            Document(page_content=x, metadata={'source': x})
            for x in text_splitter.split_text(text)
        ]
        return docs

    @staticmethod
    def _download_manifests(model):
        client = docker.from_env()
        client.containers.get(
            os.getenv('LLM_CONTAINER_NAME'),
        ).exec_run(f'ollama run {model}')

    def _select_embedding_method(self):
        if self.provider == 'HuggingFace':
            if self.model in ['all-mpnet-base-v2']:
                return HuggingFaceEmbeddings(model_name=self.model)
            elif self.model is not None:
                with st.spinner('Downloading Model Manifests...'):
                    self._download_manifests(self.model)

                return OllamaEmbeddings(base_url=os.getenv('LLM_HOST'), model=self.model)

        elif self.provider == 'OpenAI':
            if self.model is not None:
                return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_APIKEY'), model=self.model)

    @staticmethod
    def _create_engine():
        engine = create_engine(os.getenv('DATABASE_CONN_STRING'))
        return engine

    def _save_mapping(self):
        engine = self._create_engine()

        df = pd.DataFrame(
            columns=[
                'collection', 'embedding_model_provider',
                'embedding_model_name',
            ],
        )

        df['collection'] = [self.collection_name]
        df['embedding_model_provider'] = [self.provider]
        df['embedding_model_name'] = [self.model]

        df.to_sql(
            'embedding_mappings', engine,
            if_exists='append', index=False,
        )

    def __call__(self) -> Any:
        self.docs = self._chunk_docs(self.text)

        self.provider = st.selectbox(
            'Select Embedding Method', embeddings_providers,
        )
        self.model = st.selectbox(
            'Select Embedding Model', [
                None,
            ] + embeddings_models[self.provider],
        )

        self.embedding_model = self._select_embedding_method()

    def save_embeddings(self):
        Qdrant.from_documents(
            self.docs,
            self.embedding_model,
            url=os.getenv('QDRANT_HOST'),
            collection_name=self.collection_name,
        )

        self._save_mapping()
