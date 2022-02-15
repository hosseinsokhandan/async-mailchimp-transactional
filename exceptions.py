class ApiClientError(Exception):
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code