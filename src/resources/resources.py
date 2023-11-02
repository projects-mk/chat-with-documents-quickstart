import requests


class CheckResources:

    @staticmethod
    def check_qdrant():
        try:
            response = requests.get('http://localhost:6333')
            if response.status_code == 200:
                return 'Running'
        except requests.exceptions.ConnectionError:
            return 'Unavailable'
