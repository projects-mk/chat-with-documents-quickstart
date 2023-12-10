from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv
from st_pages import Page, show_pages

from utils.conf_loaders import load_config
from utils.data_loaders import StylesLoader

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

    show_pages(
        [
            Page('app/about.py', 'About', ''),
            Page('app/resources.py', 'Resources', ''),
            Page('app/chat.py', 'Chat', ''),
        ],
    )
