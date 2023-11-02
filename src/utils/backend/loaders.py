from __future__ import annotations

from langchain.document_loaders import PyPDFLoader


class Document_Loader:
    def __init__(self, filepath) -> None:
        self.filepath = filepath

    def read_pdf(self, pdf_password=None):
        reader = PyPDFLoader(self.filepath, password=pdf_password)

        return reader.load()
