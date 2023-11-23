import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from utils.data_loaders import HtmlLoader, StylesLoader
from utils.utils import CheckResources

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

    for i in avaiable_resources:
        os.environ[i] = avaiable_resources[i][0]

    st.markdown('<br>', unsafe_allow_html=True)
    st.button('Create API Key for Vector Database')
