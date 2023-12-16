import os
import time

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu

from utils.chatbot import ChatBot
from utils.conf_loaders import load_config
from utils.data_loaders import DocumentLoader, StylesLoader
from utils.preprocessing import MakeEmbeddings
from utils.utils import CheckResources


load_dotenv('../.env')
engine = create_engine(os.getenv('DATABASE_CONN_STRING'))

app_config = load_config()
app_info_texts = app_config['info_texts']
models = load_config(custom_key='models')
embeddings_methods = load_config(custom_key='embeddings')
qdrant_host = os.getenv('QDRANT_HOST')


def get_datastore_status():
    status = os.getenv('Vector Datastore')
    if status:
        return status
    return CheckResources.check_qdrant()


def generate_selectbox(col, label, options):
    return col.selectbox(label=label, options=options)


if __name__ == '__main__':
    st.set_page_config(
        page_title='DocSearch.ai',
        page_icon='📜',
        layout='wide',
        initial_sidebar_state='expanded',
    )

    css_file_path = 'templates/styles/styles.css'
    CSS = StylesLoader().load(css_file_path=css_file_path)
    st.markdown(CSS, unsafe_allow_html=True)

    if get_datastore_status() == 'Running':

        option_selected = option_menu(
            menu_title='',
            options=load_config(custom_key='chat_menu_options'),
            orientation='horizontal',
        )

        if option_selected == 'Existing Documents':

            try:
                client = QdrantClient(url=qdrant_host)
                collections_dict = {
                    index: collection.name
                    for index, collection in enumerate(
                        dict(client.get_collections())['collections'],
                    )
                }

                st.subheader('Get answers from uploaded documents')
                col1, col2, col3 = st.columns(3)
                with col1:
                    selected_collection = generate_selectbox(
                        col1, 'Collection', collections_dict.values(),
                    )
                with col2:
                    model_provider = generate_selectbox(
                        col2, 'Model provider', models.keys(),
                    )
                with col3:
                    try:
                        if model_provider == 'HuggingFace':
                            llms = pd.read_sql_table('llm_models', engine)
                            downloaded_llms = llms['model_name'].unique(
                            ).tolist()
                            model = generate_selectbox(
                                col3, 'Model', downloaded_llms,
                            )

                        elif model_provider != 'HuggingFace':
                            model = generate_selectbox(
                                col3, 'Model', models[model_provider],
                            )
                    except Exception:
                        st.markdown('<br>', unsafe_allow_html=True)
                        st.warning(
                            'Download models first. Go to Resources tab',
                        )

                df = pd.read_sql_table('embedding_mappings', engine)

                mapping = df.loc[df['collection'] == selected_collection].to_dict(orient='records')[
                    0
                ]
                embedding_model_provider = mapping['embedding_model_provider']
                embedding_model = mapping['embedding_model_name']

                bot = ChatBot(
                    selected_collection=selected_collection,
                    selected_model_provider=model_provider,
                    selected_model=model,
                    vector_db_client=client,
                    embedding_model_provider=embedding_model_provider,
                    embedding_model=embedding_model,
                )

                bot.start_chatting()
            except (KeyError, ValueError):
                st.info(app_info_texts['no_collections_found'])

            except NameError:
                # No models defined - do nothing
                pass

            except Exception:
                # No new chat initialized
                st.info('You need to initialize a new chat first')

        elif option_selected == 'Upload New Documents':
            uploaded_file = st.file_uploader(
                label='upload_new_docs',
                type=['pdf'],
                accept_multiple_files=False,
                label_visibility='hidden',
            )

            if uploaded_file:
                collection_name = st.text_input(
                    label='Collection Name',
                    value='',
                    help=app_info_texts['collections'],
                )

                uploaded_file_name = st.text_input(
                    label='Document Name',
                    value=uploaded_file.name,
                )

                bytes_data = uploaded_file.getvalue()

                doc_data = DocumentLoader(uploaded_file_name).read_pdf_from_bytes(bytes_data)

                make_embeddings = MakeEmbeddings(doc_data, collection_name)

                make_embeddings()

                if st.button(label='Upload Documents'):
                    with st.spinner(text='Uploading Documents...'):
                        make_embeddings.save_embeddings()

                    st.toast('Documents Uploaded Successfully!')
                    time.sleep(0.5)
