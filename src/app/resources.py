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


def generate_text_input(col, label, env_var, password=False):
    return col.text_input(label=label, value=os.getenv(env_var), type='password' if password else 'default')


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

    avaiable_resources = {
        'Vector Database': CheckResources.check_qdrant(),
        'App Database': CheckResources.check_db(),
        'Self-hosted LLM': CheckResources.check_llm(),
        'LLM Monitoring': CheckResources.check_monitoring(),
    }

    avaiable_resources_df = pd.DataFrame(avaiable_resources, index=[0])

    st.subheader('Available resources')
    st.dataframe(
        avaiable_resources_df.T.reset_index().rename(
            {0: 'Status', 'index': 'Resource'}, axis=1,
        ),
        use_container_width=True,
        hide_index=True,
    )

    for i in avaiable_resources:
        os.environ[i] = avaiable_resources[i]

    st.divider()

    st.subheader('Enable prompt monitoring')
    with st.form(key='prompt_monitoring') as form:
        col1, col2, col3, col4 = st.columns(4)
        connection_dict = {}
        connection_dict['LANGFUSE_SERVER_URL'] = generate_text_input(
            col1, 'Langfuse URL', 'MONITORING_SERVER_URL',
        )
        connection_dict['LANGFUSE_SECRET_KEY'] = generate_text_input(
            col2, 'Langfuse Secret Key', '', password=True,
        )
        connection_dict['LANGFUSE_PUBLIC_KEY'] = generate_text_input(
            col3, 'Langfuse Public Key', '', password=True,
        )

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
    st.subheader('Currently downloaded HuggingFace models')
    try:
        st.dataframe(
            pd.read_sql_table('llm_models', engine).drop_duplicates(
            ), use_container_width=True, hide_index=True,
        )
    except ValueError:
        st.write('No models downloaded yet')

    st.markdown('<br>', unsafe_allow_html=True)
    st.subheader('Download Huggingface LLMs')
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
