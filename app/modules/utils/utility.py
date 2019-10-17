import requests

class Utility:

    @staticmethod
    def check_internet():
        try:
            requests.head('https://www.google.com')
            return True
        except requests.exceptions.ConnectionError:
            return False    
