import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import time
from utils.data_loaders import StylesLoader
from utils.utils import CheckResources
from langfuse.callback import CallbackHandler
from sqlalchemy import create_engine
import docker

load_dotenv('../.env')
engine = create_engine(os.getenv('DATABASE_CONN_STRING'))

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

    avaiable_resources = pd.DataFrame()

    avaiable_resources['Vector Database'] = [
        CheckResources.check_qdrant(),
    ]

    avaiable_resources['App Database'] = [
        CheckResources.check_db(),
    ]

    avaiable_resources['Self-hosted LLM'] = [
        CheckResources.check_llm(),
    ]

    avaiable_resources['LLM Monitoring'] = [
        CheckResources.check_monitoring(),
    ]

    st.dataframe(
        avaiable_resources.T.reset_index().rename(
            {0: 'Status', 'index': 'Resource'}, axis=1,
        ),
        use_container_width=True,
        hide_index=True,
    )

    for i in avaiable_resources:
        os.environ[i] = avaiable_resources[i][0]

    st.divider()

    with st.expander('Enable prompt monitoring'):
        with st.form(key='prompt_monitoring') as form:
            col1, col2, col3, col4 = st.columns(4)
            connection_dict = {}
            with col1:
                connection_dict['LANGFUSE_SERVER_URL'] = st.text_input(
                    label='Langfuse URL', value=os.getenv('MONITORING_SERVER_URL'),
                )
            with col2:
                connection_dict['LANGFUSE_SECRET_KEY'] = st.text_input(
                    label='Langfuse Secret Key', value='', type='password',
                )  # sk-lf-764ee597-ef55-41d4-9ec5-50191c52eb25
            with col3:
                connection_dict['LANGFUSE_PUBLIC_KEY'] = st.text_input(
                    label='Langfuse Public Key', value='', type='password',
                )  # pk-lf-e9fd97c0-1fbb-45ce-b8af-b142ed5bc848

            with col4:
                st.markdown('<br>', unsafe_allow_html=True)
                submit = st.form_submit_button('Connect')

            if submit:

                try:
                    handler = CallbackHandler(
                        host=connection_dict['LANGFUSE_SERVER_URL'],
                        secret_key=connection_dict['LANGFUSE_SECRET_KEY'],
                        public_key=connection_dict['LANGFUSE_PUBLIC_KEY'],
                    )
                    if handler.auth_check() == True:
                        st.success('Monitoring enabled')
                        time.sleep(1)
                        with st.spinner('Updating database...'):
                            pd.DataFrame(connection_dict, index=[0]).to_sql(
                                'monitoring', engine, if_exists='replace', index=False,
                            )
                        st.rerun()
                except Exception as e:
                    st.error('Connection could not be enstablished')

    st.markdown('<br>', unsafe_allow_html=True)

    st.divider()
    st.subheader('Currently downloaded models')

    st.dataframe(
        pd.read_sql_table('llm_models', engine).drop_duplicates(
        ), use_container_width=True, hide_index=True,
    )

    st.markdown('<br>', unsafe_allow_html=True)
    with st.expander('Download Huggingface LLMs'):
        with st.form(key='model_downloader'):
            st.markdown(
                '##### Checkout this [link](https://ollama.ai/library) to see which models are currently supported', unsafe_allow_html=True,
            )

            col11, col22 = st.columns(2)
            with col11:
                model_name = st.text_input(
                    label='Model name', value='stablelm-zephyr:3b',
                )
            with col22:
                st.markdown('<br>', unsafe_allow_html=True)
                submit = st.form_submit_button('Download')

            if submit:
                client = docker.from_env()
                try:
                    with st.spinner('Downloading model files...'):
                        client.containers.get(os.getenv('LLM_CONTAINER_NAME')).exec_run(
                            f'ollama run {model_name}',
                        )
                        df = pd.DataFrame()
                        df['model_name'] = [model_name]
                        df['creation_date'] = [
                            pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
                        ]
                        df.to_sql(
                            'llm_models', engine,
                            if_exists='append', index=False,
                        )

                    st.success('Model downloaded successfully!')
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error('Model could not be downloaded')
