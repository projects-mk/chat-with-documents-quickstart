import base64
import os

import requests
import streamlit as st

from sqlalchemy import create_engine
from psycopg2.errors import OperationalError
from dotenv import load_dotenv

load_dotenv('../.env')


def clear_cache():
    st.legacy_caching.caching.clear_cache()

# flake8: noqa: E501


def show_pdf_uplaoded(bytes_data):
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="100" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


class CheckResources:
    @staticmethod
    @st.cache_data
    def check_qdrant():
        try:
            response = requests.get(os.getenv('QDRANT_HOST'))
            if response.status_code == 200:
                return 'Running'
        except requests.exceptions.ConnectionError:
            return 'Unavailable'

    def check_db():
        try:
            conn_string = os.getenv('DATABASE_CONN_STRING')
            engine = create_engine(conn_string)
            engine.connect()
            return 'Running'

        except OperationalError:
            return 'Unavailable'

    @staticmethod
    def check_llm():
        try:
            response = requests.get(os.getenv('LLM_HOST'))
            if response.status_code == 200:
                return 'Running'
        except requests.exceptions.ConnectionError:
            return 'Unavailable'
