from __future__ import annotations

import io

from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader


class DocumentLoader:
    @staticmethod
    def _read_pages(pdf_reader):
        pdf_content = ''

        for page in pdf_reader.pages:
            pdf_content += page.extract_text()

        return pdf_content

    def read_pdf_from_bytes(self, bytes_data):
        with io.BytesIO(bytes_data) as base64_pdf:
            reader = PdfReader(base64_pdf)
            doc = self._read_pages(reader)

        return doc

    @staticmethod
    def read_pdf_from_path(filepath, pdf_password=None):
        reader = PyPDFLoader(filepath, password=pdf_password)

        return reader.load()


class StylesLoader:
    def __init__(self, css_file_path: str):
        self.css_file_path = css_file_path

    def load(self):
        with open(self.css_file_path, 'r', encoding='utf-8') as f:
            css = f.read()
        return f'<style>\n\n{css}\n</style>'


class HtmlLoader:
    def load(self, html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return html
