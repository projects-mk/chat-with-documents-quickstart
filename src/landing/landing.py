from utils.load_styles import Styles
from utils.backend.pages import Page


class LandingPage(Page):
    def __init__(self):
        Styles(css_file_path='utils/styles/styles.css').load()

    def load(self, html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return html


# st.components.v1.html(html=LandingPage().load(html_file_path='landing/static/index.html'),
#                                     width=None,
#                                     height=4000,
#                                     scrolling=False)
