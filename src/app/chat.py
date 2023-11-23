import os
import time

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from streamlit_option_menu import option_menu

from utils.conf_loaders import load_config
from utils.data_loaders import DocumentLoader, StylesLoader
from utils.preprocessing import MakeEmbeddings
from utils.chatbot import ChatBot

app_config = load_config()
app_info_texts = app_config['info_texts']

models = load_config(custom_key='models')

load_dotenv('../.env')


if __name__ == '__main__':
    st.set_page_config(
        page_title='DocSearch.ai',
        page_icon='📜',
        layout='wide',
        initial_sidebar_state='expanded',
    )

    css_file_path = 'templates/styles/styles.css'
    CSS = StylesLoader(css_file_path=css_file_path).load()
    st.markdown(CSS, unsafe_allow_html=True)

    if os.getenv('Vector Datastore') == 'Running':

        option_selected = option_menu(
            menu_title='',
            options=load_config(custom_key='chat_menu_options'),
            orientation='horizontal',
        )

        if option_selected == 'Existing Documents':

            try:
                with st.expander(label='All Collections'):
                    client = QdrantClient(url=os.getenv('QDRANT_HOST'))
                    collections_dict = {
                        index: collection.name
                        for index, collection in enumerate(
                            dict(client.get_collections())['collections'],
                        )
                    }
                    collections_df = pd.DataFrame.from_dict(
                        collections_dict, orient='index',
                    ).rename({0: 'Document Store Name'}, axis=1)

                    collections_df['Metadata'] = (
                        os.getenv('QDRANT_HOST')
                        + '/dashboard#/collections/'
                        + collections_df['Document Store Name']
                    )

                    st.dataframe(
                        collections_df, use_container_width=True, hide_index=True,
                    )

                    st.link_button(
                        'Manage yours collections',
                        os.getenv('QDRANT_HOST') + '/dashboard#/collections/',
                    )

                st.subheader('Get answers from uploaded documents')
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    selected_collection = st.selectbox(
                        label='Collection', options=collections_dict.values(),
                    )
                with col2:
                    model_provider = st.selectbox(
                        label='Model provider', options=models.keys(),
                    )
                with col3:
                    model = st.selectbox(
                        label='Model', options=models[model_provider],
                    )

                with col4:
                    embdedding_method = st.selectbox(
                        label='Embedding Method', options=['OpenAI'],
                    )

                # with st.expander(label="Initial Query"):
                st.divider()
                initial_query = st.text_input(
                    label='Initial Query', value='What is this document about ?', label_visibility='hidden',
                )
                st.session_state['start_chat'] = st.button(
                    label='Start Chat', type='secondary', use_container_width=True,
                )

                if st.session_state['start_chat']:
                    st.divider()

                    bot = ChatBot(
                        initial_query=initial_query,
                        selected_collection=selected_collection,
                        selected_model=model,
                        vector_db_client=client,
                        embedding_method=embdedding_method,
                    )

                    bot.start_chatting()

            except KeyError:
                st.write(app_info_texts['no_collections_found'])

        elif option_selected == 'Upload New Documents':
            docs = st.file_uploader(
                label='upload_new_docs',
                type=['pdf'],
                accept_multiple_files=False,
                label_visibility='hidden',
            )
            if docs:
                collection_name = st.text_input(
                    label='Collection Name',
                    value='',
                    help=app_info_texts['collections'],
                )

                bytes_data = docs.getvalue()

                text = DocumentLoader().read_pdf_from_bytes(bytes_data)

                make_embeddings = MakeEmbeddings(text, collection_name)

                make_embeddings()

                if st.button(label='Upload Documents'):
                    with st.spinner(text='Uploading Documents...'):
                        make_embeddings.save_embeddings()

                    st.toast('Documents Uploaded Successfully!')
                    time.sleep(0.5)
