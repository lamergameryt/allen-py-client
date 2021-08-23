import requests

__all__ = ['AllenInvalidUsernamePassword', 'AllenInvalidResponse', 'AllenResponseUnavailable']


class AllenInvalidUsernamePassword(Exception):
    """
    Exception representing an invalid username or password entered.
    """

    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return 'Invalid username or password entered'


class AllenResponseUnavailable(Exception):
    """
    Exception representing a failed request to a resource.
    """

    def __init__(self, url: str, response: requests.Response):
        super().__init__(self)
        self._url = url
        self._response = response

    def __str__(self):
        status = self._response.status_code
        return f'{self._url} : (HTTP Status: {status})'


class AllenInvalidResponse(Exception):
    """
    Exception representing a corrupted / unexpected response received from the server.
    """

    def __init__(self, response: requests.Response):
        super().__init__(self)
        self._response = response

    def __str__(self):
        status_code = self._response.status_code
        url = self._response.request.url
        return f'{url} (Status Code : {status_code})'
