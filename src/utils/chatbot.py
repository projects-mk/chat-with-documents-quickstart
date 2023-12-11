import os

import docker
import pandas as pd
import streamlit as st
from langchain.chains.qa_with_sources.retrieval import \
    RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import (
    HuggingFaceEmbeddings, OllamaEmbeddings,
    OpenAIEmbeddings,
)
from langchain.llms import Ollama
from langchain.memory import PostgresChatMessageHistory
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from sqlalchemy import create_engine
from langfuse.callback import CallbackHandler


class ChatBot:
    def __init__(
        self, selected_collection,
        selected_model_provider,
        selected_model,
        vector_db_client,
        embedding_model_provider,
        embedding_model,
    ) -> None:

        self.mapping = {'ai': 'assistant', 'human': 'user'}
        self.selected_collection = selected_collection
        self.vector_db_client = vector_db_client
        self.selected_model_provider = selected_model_provider
        self.selected_model = selected_model
        self.embedding_model_provider = embedding_model_provider
        self.embedding_model = embedding_model

    def _select_embedding_method(self, provider, model):
        if model is not None:
            if provider == 'HuggingFace':
                return HuggingFaceEmbeddings(model_name=model)

            elif provider == 'OpenAI':
                return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_APIKEY'), model=model)

    @staticmethod
    def _select_model_params(self):
        self.model_temperature = st.slider('Temperature', 0.0, 1.0, 0.01)

    def _setup_llm(self):
        if self.selected_model_provider == 'HuggingFace':

            llm = Ollama(
                model=self.selected_model,
                base_url=os.getenv('LLM_HOST'),
            )

            return llm

        elif self.selected_model_provider == 'OpenAI':
            llm = ChatOpenAI(
                model=self.selected_model, temperature=0.5,
                openai_api_key=os.getenv('OPENAI_APIKEY'),
                verbose=True,
            )
            return llm

    def _connect_vector_db(self, embeddings):
        vectordb = QdrantClient(url=os.getenv('QDRANT_HOST'))
        vectordb = Qdrant(
            client=self.vector_db_client,
            collection_name=self.selected_collection,
            embeddings=embeddings,
        )
        return vectordb

    @staticmethod
    def _clear_chat(chat_history):
        with st.sidebar:
            if st.button('Reset converstaion', use_container_width=True):
                chat_history.clear()
                st.rerun()

    def _configure_qa_chain(self, llm, vector_db):
        qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            retriever=vector_db.as_retriever(
                search_type='similarity',
            ),
            verbose=True,
        )

        return qa_chain

    @staticmethod
    def _create_new_chat_window():
        connection_string = os.getenv('DATABASE_CONN_STRING')
        engine = create_engine(connection_string)

        with st.expander('Create New Chat'):
            form = st.form(key='new_chat_creation')

            session_id = form.text_input(
                label='New Chat', label_visibility='hidden', value='New Chat',
            )
            create = form.form_submit_button(
                'Create', use_container_width=True,
            )

            if create:
                df = pd.DataFrame()
                df['chat_name'] = [session_id]
                df['creation_date'] = [
                    pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
                ]
                df.to_sql(
                    'chat_sessions', engine,
                    if_exists='append', index=False,
                )
                st.toast('Chat Created Successfully!')
                st.rerun()

    def _get_chat_session_id(self):
        with st.sidebar:
            try:
                all_chats = pd.read_sql_table(
                    'chat_sessions', os.getenv('DATABASE_CONN_STRING'),
                )
                chat_id = st.selectbox(
                    'Select Chat', all_chats['chat_name'].unique(),
                )
                self._create_new_chat_window()
                return chat_id
            except ValueError:
                self._create_new_chat_window()
            st.divider()

    @staticmethod
    def _print_sources(sources):
        with st.expander('Sources'):
            st.write(sources)

    def start_chatting(self):

        embeddings = self._select_embedding_method(
            self.embedding_model_provider, self.embedding_model,
        )

        # Connect with Vector DB
        with st.spinner('Connecting to Vector DB...'):
            semantic_search = self._connect_vector_db(embeddings=embeddings)

        # Setup llm
        with st.spinner('Loading Language Model...'):
            llm = self._setup_llm()

        # Configure LLM chain
        with st.spinner('Configuring QA chain...'):
            qa_chain = self._configure_qa_chain(
                llm=llm,
                vector_db=semantic_search,
            )

        current_chat = self._get_chat_session_id()

        # Initialize conversational history
        history = PostgresChatMessageHistory(
            connection_string=os.getenv('DATABASE_CONN_STRING'),
            session_id=current_chat,
        )

        # Add chat history to sidebar button
        self._clear_chat(history)

        # Print each message in chat field
        for msg in history.messages:
            st.chat_message(self.mapping[msg.type]).write(msg.content)

        # Wait for user input
        if prompt := st.chat_input(placeholder='Tell me more about this document'):
            history.add_user_message(prompt)

            st.chat_message('user').write(prompt)

            with st.spinner('Thinking...'):
                # If user provides input, run the QA chain
                try:
                    if self.mapping[[msg.type for msg in history.messages][-1]] == 'user':
                        response = qa_chain(prompt)
                        answer = response['answer']
                        sources = response['sources']

                        history.add_ai_message(answer)
                        st.chat_message('assistant').write(answer)
                        self._print_sources(sources)

                # There are no messages in the chat written by user, do nothing
                except IndexError:
                    pass
