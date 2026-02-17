# inwx_cli/config.py

import os
import sys
import stat
import getpass
import tomllib
from pathlib import Path
from .secrets import SecretStore

CONFIG_DIR = Path.home() / ".config" / "inwx"
CONFIG_FILE = CONFIG_DIR / "config.toml"


# -----------------------------
# Helpers
# -----------------------------
def load_config(check_permissions: bool = False) -> dict:
    if not CONFIG_FILE.exists():
        return {}

    if check_permissions and not check_config_permissions():
        print(
            "WARNING: Config file permissions too open! Should be 600.",
            file=sys.stderr,
        )

    with open(CONFIG_FILE, "rb") as f:
        return tomllib.load(f)


def check_config_permissions() -> bool:
    """
    Check whether config file permissions are secure (600).

    Returns True if OK, False otherwise.
    """
    if not CONFIG_FILE.exists():
        return True

    mode = CONFIG_FILE.stat().st_mode
    return not (mode & (stat.S_IRWXG | stat.S_IRWXO))


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

    config = {
        "default_account": account,
        account: {
            "username": username,
        }
    }

    SecretStore.set_password(account, password)

    if secret:
        SecretStore.set_shared_secret(account, secret)

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

    config[account] = {
        "username": username,
    }

    SecretStore.set_password(account, password)

    if secret:
        SecretStore.set_shared_secret(account, secret)

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

    SecretStore.del_password(account)
    SecretStore.del_shared_secret(account)
    del config[account]

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

    for account, value in config.items():
        if not isinstance(value, dict):
            continue

        marker = " (default)" if account == default else ""
        print(f"- {account}{marker}")

        username = value.get("username")
        print(f"  username: {username or 'missing ✘'} ✔")

        has_password = bool(SecretStore.get_password(account))
        has_secret = bool(SecretStore.get_shared_secret(account))

        print(f"  password: {'stored in keyring ✔' if has_password else 'not set ✘'}")
        print(f"  shared_secret: {'stored in keyring ✔' if has_secret else 'not set ✘'}")
        print()

def config_doctor(args):
    config = load_config()
    errors = 0
    warnings = 0

    print("INWX CLI configuration doctor\n")

    # -----------------------------
    # Config file checks
    # -----------------------------
    if not CONFIG_FILE.exists():
        print("Config file:")
        print(f"  path: {CONFIG_FILE}")
        print("  status: missing ✘\n")
        return 2

    mode = CONFIG_FILE.stat().st_mode
    perm_ok = not (mode & (stat.S_IRWXG | stat.S_IRWXO))

    print("Config file:")
    print(f"  path: {CONFIG_FILE}")
    print(f"  permissions: {'600 ✔' if perm_ok else 'should be 600 ✘'}")
    if not perm_ok:
        warnings += 1
    print()

    # -----------------------------
    # Accounts
    # -----------------------------
    print("Accounts:")

    accounts = [k for k, v in config.items() if isinstance(v, dict)]

    if not accounts:
        print("  no accounts configured ✘\n")
        return 2

    for account in accounts:
        entry = config[account]
        print(f"- {account}")

        username = entry.get("username")
        if username:
            print("  username: ✔")
        else:
            print("  username: missing ✘")
            errors += 1

        pwd = SecretStore.get_password(account)
        if pwd:
            print("  password (keyring): ✔")
        else:
            print("  password (keyring): missing ✘")
            errors += 1

        secret = SecretStore.get_shared_secret(account)
        if secret:
            print("  shared_secret (keyring): ✔")
        else:
            print("  shared_secret (keyring): not set ✘")
            warnings += 1

        print()

    # -----------------------------
    # Default account
    # -----------------------------
    default = config.get("default_account")
    print("Default account:")

    if not default:
        print("  not set ✘")
        warnings += 1
    elif default not in accounts:
        print(f"  ✘ '{default}' does not exist")
        errors += 1
    else:
        print(f"  {default} ✔")

    print()

    # -----------------------------
    # Summary
    # -----------------------------
    print("Summary:")
    print(f"  errors: {errors}")
    print(f"  warnings: {warnings}")

    if errors:
        return 2
    if warnings:
        return 1
    return 0
