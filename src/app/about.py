import streamlit as st

from utils.data_loaders import HtmlLoader, StylesLoader

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

    html_path = 'templates/static/landing.html'
    html_page = HtmlLoader().load(html_file_path=html_path)
    st.components.v1.html(
        html=html_page, height=1000, scrolling=False,
    )
