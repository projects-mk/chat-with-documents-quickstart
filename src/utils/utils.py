import base64

import streamlit as st


def clear_cache():
    st.legacy_caching.caching.clear_cache()

# flake8: noqa: E501


def show_pdf_uplaoded(bytes_data):
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="100" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
