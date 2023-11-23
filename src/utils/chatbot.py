from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from qdrant_client import QdrantClient
import os
from langchain.chat_models import ChatOpenAI
import streamlit as st


class ChatBot:
    def __init__(self, initial_query, selected_collection, selected_model, vector_db_client, embedding_method) -> None:
        self.initial_query = initial_query
        self.selected_collection = selected_collection
        self.vector_db_client = vector_db_client
        self.selected_model = selected_model
        self.embedding_method = embedding_method

    @staticmethod
    def _select_embedding_method(method):
        if method == 'HuggingFace':
            return HuggingFaceEmbeddings()
        elif method == 'OpenAI':
            return OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_APIKEY'))

    @staticmethod
    def _select_model_params():
        pass

    def start_chatting(self):

        embeddings = self._select_embedding_method(self.embedding_method)

        semantic_search = QdrantClient(url=os.getenv('QDRANT_HOST'))

        semantic_search = Qdrant(
            client=self.vector_db_client,
            collection_name=self.selected_collection,
            embeddings=embeddings,
        )

        llm = ChatOpenAI(model=self.selected_model, temperature=0.5,
                         openai_api_key=os.getenv('OPENAI_APIKEY'))

        retrieval_chain = RetrievalQA.from_chain_type(
            llm,
            chain_type='stuff',
            retriever=semantic_search.as_retriever(
                search_type='similarity',
            ),
        )

        if 'messages' not in st.session_state:
            st.session_state['messages'] = [
                {'role': 'user', 'content': self.initial_query},
            ]

        # with st.container():/
        for msg in st.session_state.messages:
            st.chat_message(msg['role']).write(msg['content'])

        if prompt := st.chat_input(
            placeholder='What this document is about ?',
        ):
            st.session_state.messages.append(
                {'role': 'user', 'content': prompt},
            )

        with st.chat_message('assistant'):
            if st.session_state.messages[-1]['role'] == 'user':
                query = st.session_state.messages[-1]['content']
                response = retrieval_chain.run(query)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response},
                )
                st.write(response)
