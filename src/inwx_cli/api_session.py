# inwx_cli/api_session.py

import time
from INWX.Domrobot import ApiClient


class INWXSession:
    """
    INWX login session logic
    """

    def __init__(self, api_url, username, password, shared_secret=None):
        self.api = ApiClient(api_url=api_url, debug_mode=False)
        self.username = username
        self.password = password
        self.shared_secret = shared_secret

    def __enter__(self):
        result = self.api.login(
            self.username,
            self.password,
            self.shared_secret
        )

        if result.get("code") != 1000:
            raise Exception(result)

        return self.api

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            result = self.api.logout()
            if result.get("code") != 1500:
                print(result)
        except Exception as e:
            print(e)
