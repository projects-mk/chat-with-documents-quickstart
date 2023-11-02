class Styles:
    def __init__(self, css_file_path: str):
        self.css_file_path = css_file_path

    def load(self):
        return f'<style>\n{self.css_file_path}\n</style>'
