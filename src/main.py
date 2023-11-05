from __future__ import annotations

import os
import time

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from qdrant_client import QdrantClient

from app.resources import CheckResources
from utils.conf_loaders import load_config
from utils.data_loaders import DocumentLoader, StylesLoader, HtmlLoader
from utils.preprocessing import MakeEmbeddings

app_config = load_config()
app_info_texts = app_config['info_texts']

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
    about, resources, chat = st.tabs(app_config['main_menu_options'])

    with about:
        html_path = 'templates/static/landing.html'
        html_page = HtmlLoader().load(html_file_path=html_path)
        st.components.v1.html(
            html=html_page, height=1000, scrolling=False,
        )

    with resources:
        avaiable_resources = pd.DataFrame()

        avaiable_resources['Vector Datastore'] = [
            CheckResources.check_qdrant(),
        ]
        avaiable_resources['Database'] = [CheckResources.check_database()]

        if os.getenv('K8S_DEPLOYMENT') != 'False':
            avaiable_resources['Cluster'] = [CheckResources.check_cluster()]

        st.dataframe(
            avaiable_resources.T.reset_index().rename(
                {0: 'Status', 'index': 'Resource'}, axis=1,
            ),
            use_container_width=True,
            hide_index=True,
        )

    with chat:
        if avaiable_resources['Vector Datastore'][0] == 'Running':

            existing_docs, upload_new_docs = st.tabs(
                load_config(custom_key='chat_menu_options'),
            )

            with existing_docs:

                try:
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
                        os.getenv('QDRANT_HOST') + '/dashboard#/collections/' +
                        collections_df['Document Store Name']
                    )

                    st.dataframe(
                        collections_df,
                        use_container_width=True,
                        hide_index=True,
                    )

                except KeyError:
                    st.write(app_info_texts['no_collections_found'])

            with upload_new_docs:
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

                        st.success('Documents Uploaded Successfully!')
                        time.sleep(0.5)
                        st.rerun()
