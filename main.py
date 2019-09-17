import requests
import json
import pandas

class TBA:
    """

    Wrapper for interacting with www.thebluealliance.com

    """

    READ_URL_BASE = 'https://www.thebluealliance.com/api/v3/'
    session = requests.Session()

    def __init__(self, auth_key):
        """
        Store auth key so we can reuse it as many times as we make a request.
        :param auth_key: Your application authorization key, obtainable at https://www.thebluealliance.com/account.
        """

        self.session.headers.update({'X-TBA-Auth-Key': auth_key})

    def _get(self, url):
        """
        Helper method: GET data from given URL on TBA's API.
        :param url: URL string to get data from.
        :return: Requested data in JSON format.
        """
        return self.session.get(self.READ_URL_BASE + url).json()
