# inwx_cli/config.py

import os
import getpass
import tomllib

from pathlib import Path
from .secrets import SecretStore


CONFIG_DIR = Path.home() / ".config" / "inwx"
CONFIG_FILE = CONFIG_DIR / "config.toml"


# -----------------------------
# Helpers
# -----------------------------

def load_config():
    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "rb") as f:
        return tomllib.load(f)


def write_config(content: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        f.write(content)

    os.chmod(CONFIG_FILE, 0o600)


def serialize_config(config: dict) -> str:
    lines = []

    if "default_account" in config:
        lines.append(f'default_account = "{config["default_account"]}"\n')

    for key, value in config.items():
        if not isinstance(value, dict):
            continue

        lines.append(f"\n[{key}]")
        for k, v in value.items():
            lines.append(f'{k} = "{v}"')

    return "\n".join(lines) + "\n"


# -----------------------------
# Commands
# -----------------------------

def config_init(args):
    if CONFIG_FILE.exists():
        print(f"Config already exists at: {CONFIG_FILE}")
        return

    print("Initializing INWX configuration...\n")

    account = input("Account name: ").strip()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    secret = getpass.getpass("Shared Secret (optional): ")

    SecretStore.set(account, password)

    config = {
        "default_account": account,
        account: {
            "username": username,
            "password_ref": account,
        }
    }

    if secret:
        config[account]["shared_secret"] = secret

    write_config(serialize_config(config))

    print(f"\nConfig written to {CONFIG_FILE}")
    print("Permissions set to 600.")


def config_add(args):
    config = load_config()

    print("Add new INWX account\n")

    account = input("Account name: ").strip()

    if account in config:
        print(f"Account '{account}' already exists.")
        return

    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    secret = getpass.getpass("Shared Secret (optional): ")

    SecretStore.set(account, password)

    config[account] = {
        "username": username,
        "password_ref": account,
    }

    if secret:
        config[account]["shared_secret"] = secret

    write_config(serialize_config(config))

    print(f"\nAccount '{account}' added successfully.")


def config_remove(args):
    config = load_config()

    if not config:
        print("No configuration found.")
        return

    account = args.account

    if account not in config or not isinstance(config.get(account), dict):
        print(f"Account '{account}' does not exist.")
        return

    confirm = input(f"Really remove account '{account}'? (y/N): ").lower()

    if confirm != "y":
        print("Aborted.")
        return

    SecretStore.delete(account)
    del config[account]

    # Wenn Default entfernt wurde → löschen
    if config.get("default_account") == account:
        config.pop("default_account", None)
        print("Removed default_account setting.")

    write_config(serialize_config(config))

    print(f"Account '{account}' removed.")


def config_set_default(args):
    config = load_config()

    if not config:
        print("No configuration found.")
        return

    account = args.account

    if account not in config or not isinstance(config.get(account), dict):
        print(f"Account '{account}' does not exist.")
        return

    config["default_account"] = account

    write_config(serialize_config(config))

    print(f"Default account set to '{account}'.")


def config_list(args):
    config = load_config()

    if not config:
        print("No configuration found.")
        return

    default = config.get("default_account")

    print("Configured INWX accounts:\n")

    for key, value in config.items():
        if not isinstance(value, dict):
            continue

        marker = " (default)" if key == default else ""
        print(f" - {key}{marker}")
