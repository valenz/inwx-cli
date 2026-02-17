# inwx_cli/api_session.py

from INWX.Domrobot import ApiClient
from .exceptions import INWXAPIError
from .secrets import SecretStore


class INWXSession:
    """
    INWX login session logic
    """

    def __init__(self, api_url, account, username):
        self.api = ApiClient(api_url=api_url, debug_mode=False)
        self.account = account
        self.username = username

    def __enter__(self):
        password = SecretStore.get_password(self.account)
        secret = SecretStore.get_shared_secret(self.account)

        if not password:
            raise RuntimeError(f"Missing password in keyring for account '{self.account}'")

        result = self.api.login(
            self.username,
            password,
            secret
        )

        if result.get("code") != 1000:
            raise INWXAPIError(result)

        return self.api

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = self.api.logout()
        if result.get("code") != 1500:
            raise INWXAPIError(result)
