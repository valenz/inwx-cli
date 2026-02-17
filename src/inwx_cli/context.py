# inwx_cli/context.py

from .api_session import INWXSession


class CLIContext:
    """
    Runtime context for CLI execution.
    Holds config, account and API session.
    """

    def __init__(self, config, account, username):
        self.config = config
        self.account = account
        self.username = username
        self.session = None

    def __enter__(self):
        self.session = INWXSession(
            api_url="https://api.domrobot.com",
            account=self.account,
            username=self.username,
        )
        return self.session.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.session.__exit__(exc_type, exc_val, exc_tb)
