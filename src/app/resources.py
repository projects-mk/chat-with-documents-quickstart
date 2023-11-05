import os

import requests
import streamlit as st

import kubernetes


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
            response = requests.get(os.getenv('DATABASE_HOST'))
            if response.status_code == 200:
                return 'Running'
        except requests.exceptions.ConnectionError:
            return 'Unavailable'
