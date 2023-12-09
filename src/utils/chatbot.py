import os

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.memory import (
    ConversationBufferMemory,
    StreamlitChatMessageHistory,
)
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
import os
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
import streamlit as st


class ChatBot:
    def __init__(self, selected_collection, selected_model_provider, selected_model, vector_db_client, embedding_method) -> None:
        self.selected_collection = selected_collection
        self.vector_db_client = vector_db_client
        self.selected_model_provider = selected_model_provider
        self.selected_model = selected_model
        self.embedding_method = embedding_method

    @staticmethod
    def _select_embedding_method(method):
        if method == 'HuggingFace':
            return HuggingFaceEmbeddings()
        elif method == 'OpenAI':
            return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_APIKEY'))

    @staticmethod
    def _select_model_params(self):
        self.model_temperature = st.slider('Temperature', 0.0, 1.0, 0.01)

    def _setup_llm(self):
        if self.selected_model_provider == 'HuggingFace':
            llm = HuggingFaceHub(
                repo_id=self.selected_model,
                model_kwargs={'temperature': 0.5, 'max_length': 64},
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

    def _configure_qa_chain(self, llm, vector_db):
        # Setup memory for llm
        msgs = StreamlitChatMessageHistory()
        memory = ConversationBufferMemory(
            memory_key='chat_history', chat_memory=msgs, return_messages=True,
        )

        # Instantiate QA chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            chain_type='stuff',
            retriever=vector_db.as_retriever(
                search_type='similarity',
            ),
            memory=memory,
            verbose=True,
        )

        return qa_chain

    def start_chatting(self):

        embeddings = self._select_embedding_method(self.embedding_method)

        # Connect with Vector DB
        with st.spinner('Connecting to Vector DB...'):
            semantic_search = self._connect_vector_db(embeddings=embeddings)

        # Setup llm
        with st.spinner('Loading Language Model...'):
            llm = self._setup_llm()

        # Configure LLM chain
        with st.spinner('Configuring QA chain...'):
            qa_chain = self._configure_qa_chain(
                llm=llm, vector_db=semantic_search,
            )

        # Initialize conversational history
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [
                {'role': 'assistant', 'content': 'Hi, how can I help you?'},
            ]

        # Print each message in chat field
        for msg in st.session_state.messages:
            st.chat_message(msg['role']).write(msg['content'])

        # Wait for user input
        if prompt := st.chat_input(placeholder='Tell me more about this document'):
            st.session_state.messages.append(
                {'role': 'user', 'content': prompt},
            )
            st.chat_message('user').write(prompt)

            with st.spinner('Thinking...'):
                # If user provides input, run the QA chain
                try:
                    if st.session_state.messages[-1]['role'] == 'user':
                        response = qa_chain.run(prompt)
                        st.session_state.messages.append(
                            {'role': 'assistant', 'content': response},
                        )
                        st.chat_message('assistant').write(response)

                # There are no messages in the chat written by user, do nothing
                except IndexError:
                    pass
