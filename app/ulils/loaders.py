from __future__ import annotations

from pypdf import PdfReader


class Document_Loader:

    @staticmethod
    def read_pdf(doc_path, pdf_password=None):
        reader = PdfReader(doc_path, password=pdf_password)

        whole_doc = ''
        for page in range(len(reader.pages)):
            whole_doc += reader.pages[page].extract_text()
        return whole_doc
