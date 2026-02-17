# inwx_cli/secrets.py

import keyring


class SecretStore:
    SERVICE = "inwx-cli"

    @classmethod
    def set_password(cls, account: str, password: str):
        keyring.set_password(cls.SERVICE, f"{account}:password", password)

    @classmethod
    def get_password(cls, account: str) -> str | None:
        return keyring.get_password(cls.SERVICE, f"{account}:password")

    @classmethod
    def del_password(cls, account: str) -> None:
        try:
            keyring.delete_password(cls.SERVICE, f"{account}:password")
        except keyring.errors.PasswordDeleteError:
            pass  # secret did not exist → fine

    @classmethod
    def set_shared_secret(cls, account: str, secret: str):
        keyring.set_password(cls.SERVICE, f"{account}:shared_secret", secret)

    @classmethod
    def get_shared_secret(cls, account: str) -> str | None:
        return keyring.get_password(cls.SERVICE, f"{account}:shared_secret")

    @classmethod
    def del_shared_secret(cls, account: str) -> None:
        try:
            keyring.delete_password(cls.SERVICE, f"{account}:shared_secret")
        except keyring.errors.PasswordDeleteError:
            pass

