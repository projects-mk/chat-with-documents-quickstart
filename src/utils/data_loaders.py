import io

from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader


class DocumentLoader:
    """
    This class provides methods to load documents from PDF files.
    """

    @staticmethod
    def _read_pages(pdf_reader):
        """
        Reads the text from all pages of a PDF file.

        Args:
            pdf_reader (PdfReader): The PDF reader object.

        Returns:
            str: The text extracted from the PDF.
        """
        pdf_content = ''

        for page in pdf_reader.pages:
            pdf_content += page.extract_text()

        return pdf_content

    @staticmethod
    def read_pdf_from_bytes(bytes_data):
        """
        Reads a PDF file from bytes data.

        Args:
            bytes_data (bytes): The bytes data of the PDF file.

        Returns:
            str: The text extracted from the PDF.
        """
        with io.BytesIO(bytes_data) as base64_pdf:
            reader = PdfReader(base64_pdf)
            doc = DocumentLoader._read_pages(reader)

        return doc

    @staticmethod
    def read_pdf_from_path(filepath, pdf_password=None):
        """
        Reads a PDF file from a file path.

        Args:
            filepath (str): The path to the PDF file.
            pdf_password (str, optional): The password for the PDF file. Defaults to None.

        Returns:
            str: The text extracted from the PDF.
        """
        reader = PyPDFLoader(filepath, password=pdf_password)

        return reader.load()


class StylesLoader:
    """
    This class provides methods to load CSS styles from a file.
    """

    @staticmethod
    def load(css_file_path):
        """
        Loads CSS styles from a file.

        Args:
            css_file_path (str): The path to the CSS file.

        Returns:
            str: The CSS styles.
        """
        with open(css_file_path, 'r', encoding='utf-8') as f:
            css = f.read()
        return f'<style>\n\n{css}\n</style>'


class HtmlLoader:
    """
    This class provides methods to load HTML from a file.
    """

    @staticmethod
    def load(html_file_path):
        """
        Loads HTML from a file.

        Args:
            html_file_path (str): The path to the HTML file.

        Returns:
            str: The HTML content.
        """
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return html
