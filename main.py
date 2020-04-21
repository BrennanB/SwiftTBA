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

    @staticmethod
    def team_key(identifier):
        """
        Take raw team number or string key and return string key.
        Used by all team-related methods to support either an integer team number or team key being passed.
        (We recommend passing an integer, just because it's cleaner. But whatever works.)
        :param identifier: int team number or str 'frc####'
        :return: string team key in format 'frc####'
        """
        return identifier if type(identifier) == str else 'frc%s' % identifier

    def teams(self, page=None, year=None, simple=False, keys=False):
        """
        Get list of teams.
        :param page: Page of teams to view. Each page contains 500 teams.
        :param year: View teams from a specific year.
        :param simple: Get only vital data.
        :param keys: Set to true if you only want the teams' keys rather than full data on them.
        :return: List of Team objects or string keys.
        """
        # If the user has requested a specific page, get that page.
        if page is not None:
            if year:
                if keys:
                    return self._get('teams/%s/%s/keys' % (year, page))
                else:
                    return [Team(raw) for raw in self._get('teams/%s/%s%s' % (year, page, '/simple' if simple else ''))]
            else:
                if keys:
                    return self._get('teams/%s/keys' % page)
                else:
                    return [Team(raw) for raw in self._get('teams/%s%s' % (page, '/simple' if simple else ''))]
        # If no page was specified, get all of them and combine.
        else:
            teams = []
            target = 0
            while True:
                page_teams = self.teams(page=target, year=year, simple=simple, keys=keys)
                if page_teams:
                    teams.extend(page_teams)
                else:
                    break
                target += 1
            return teams