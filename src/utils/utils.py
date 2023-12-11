import base64
import os

import requests
import streamlit as st
from dotenv import load_dotenv
from psycopg2.errors import OperationalError
from sqlalchemy import create_engine
from langfuse.callback import CallbackHandler
import pandas as pd

load_dotenv('../.env')


def clear_cache():
    """
    Clears the cache in the Streamlit app.
    """
    st.legacy_caching.caching.clear_cache()


def show_pdf_uplaoded(bytes_data):
    """
    Displays the uploaded PDF in the Streamlit app.

    Args:
        bytes_data (bytes): The binary data of the PDF.
    """
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="100" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


class CheckResources:
    """
    This class provides methods to check the status of various resources.
    """

    @staticmethod
    @st.cache_data
    def check_service(service_url):
        """
        Checks the status of a service at the given URL.

        Args:
            service_url (str): The URL of the service to check.

        Returns:
            str: 'Running' if the service is available, 'Unavailable' otherwise.
        """
        try:
            response = requests.get(service_url)
            if response.status_code == 200:
                return 'Running'
        except requests.exceptions.ConnectionError:
            return 'Unavailable'

    @staticmethod
    def check_qdrant():
        """
        Checks the status of the Qdrant service.

        Returns:
            str: 'Running' if the service is available, 'Unavailable' otherwise.
        """
        return CheckResources.check_service(os.getenv('QDRANT_HOST'))

    @staticmethod
    def check_llm():
        """
        Checks the status of the LLM service.

        Returns:
            str: 'Running' if the service is available, 'Unavailable' otherwise.
        """
        return CheckResources.check_service(os.getenv('LLM_HOST'))

    @staticmethod
    def create_and_check_db_conn(conn_string):
        """
        Creates a database connection and checks its status.

        Args:
            conn_string (str): The connection string for the database.

        Returns:
            str: 'Running' if the connection is successful, 'Unavailable' otherwise.
        """
        try:
            engine = create_engine(conn_string)
            engine.connect()
            return 'Running'
        except OperationalError:
            return 'Unavailable'

    @staticmethod
    def check_db():
        """
        Checks the status of the database connection.

        Returns:
            str: 'Running' if the connection is successful, 'Unavailable' otherwise.
        """
        return CheckResources.create_and_check_db_conn(os.getenv('DATABASE_CONN_STRING'))

    @staticmethod
    def check_monitoring():
        """
        Checks the status of the monitoring service.

        Returns:
            str: 'Running' if the service is available, 'Unavailable' otherwise.
        """
        conn_string = os.getenv('DATABASE_CONN_STRING')
        engine = create_engine(conn_string)
        df = pd.read_sql_table('monitoring', engine)
        monitoring_dict = df.to_dict(orient='records')[0]
        print(monitoring_dict)
        try:
            handler = CallbackHandler(
                host=monitoring_dict['LANGFUSE_SERVER_URL'],
                public_key=monitoring_dict['LANGFUSE_PUBLIC_KEY'],
                secret_key=monitoring_dict['LANGFUSE_SECRET_KEY'],
            )

            if handler.auth_check() == True:
                return 'Running'
        except Exception as e:
            return 'Unavailable'
