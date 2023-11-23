import base64
import os

import requests
import streamlit as st

import kubernetes
import psycopg2
from psycopg2.errors import OperationalError


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

    @staticmethod
    @st.cache_data
    def check_cluster():
        try:
            kubernetes.config.load_kube_config()
            api = kubernetes.client.CoreV1Api()
            api.list_namespaced_pod(namespace='default')
            return 'Running'
        except kubernetes.config.config_exception.ConfigException:
            return 'Unavailable'

    @staticmethod
    @st.cache_data
    def check_database():
        try:
            response = psycopg2.connect(
                host=os.getenv('DATABASE_HOST'),
                port='5432',
                password=os.getenv('POSTGRES_PASSWORD'),
                user=os.getenv('POSTGRES_USER'),
                database='postgres',
            )
            if response.code:
                return 'Running'
        except OperationalError:
            return 'Unavailable'
