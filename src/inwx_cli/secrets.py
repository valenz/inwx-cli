import keyring

SERVICE_NAME = "inwx-cli"


class SecretStore:
    @staticmethod
    def set(account: str, password: str) -> None:
        keyring.set_password(SERVICE_NAME, account, password)

    @staticmethod
    def get(account: str) -> str:
        password = keyring.get_password(SERVICE_NAME, account)
        if not password:
            raise RuntimeError(
                f"No password found in keyring for account '{account}'"
            )
        return password

    @staticmethod
    def delete(account: str) -> None:
        keyring.delete_password(SERVICE_NAME, account)
