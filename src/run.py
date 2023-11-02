from __future__ import annotations

import streamlit as st
from landing.landing import LandingPage
from resources.resources import CheckResources
from utils.backend.conf_loaders import load_config
from utils.styles.styles import CSS
import pandas as pd
# from st_pages import Page, show_pages, add_page_title

if __name__ == '__main__':
    st.set_page_config(
        page_title='DocSearch.ai',
        page_icon='📜',
        layout='wide',
        initial_sidebar_state='expanded',
    )

    st.markdown(CSS, unsafe_allow_html=True)
    about, resources, reader = st.tabs(
        load_config(custom_key='main_menu_options'),
    )

    with about:
        st.components.v1.html(
            html=LandingPage().load(
                html_file_path='utils/static/landing.html',
            ), height=1000, scrolling=False,
        )

    with resources:
        resources_dict = {'Vector Datastore': CheckResources.check_qdrant()}
        # st.write(resources_dict)
        avaiable_resources = pd.DataFrame(data=resources_dict, index=[0])
        st.components.v1.html(
            avaiable_resources.T.rename(
                {0: 'Status'}, axis=1,
            ).to_html(),
        )
