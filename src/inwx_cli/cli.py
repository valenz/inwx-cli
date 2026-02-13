# inwx_cli/cli.py

import argparse
import json
import sys
import os
import stat
import tomllib

from pathlib import Path
from .config import (
    config_init,
    config_add,
    config_list,
    config_set_default,
    config_remove,)
from .context import CLIContext
from .api_core import register_methods
from .api_methods.nameserver import METHODS as NAMESERVER_METHODS
from .api_methods.domain import METHODS as DOMAIN_METHODS


# -----------------------------
# Helpers
# -----------------------------
def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def load_config():
    config_path = Path.home() / ".config" / "inwx" / "config.toml"

    if not config_path.exists():
        return {}

    mode = config_path.stat().st_mode
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        print("WARNING: Config file permissions too open! Should be 600.", file=sys.stderr)

    with open(config_path, "rb") as f:
        return tomllib.load(f)


def get_credentials(config, account):
    env_user = os.environ.get(f"INWX_USER_{account.upper()}")
    env_pass = os.environ.get(f"INWX_PASS_{account.upper()}")
    env_secret = os.environ.get(f"INWX_SECRET_{account.upper()}")

    if env_user and env_pass:
        return env_user, env_pass, env_secret

    if account in config:
        return (
            config[account].get("username"),
            config[account].get("password"),
            config[account].get("shared_secret"),
        )

    return None, None, None


def resolve_account(args, config):
    if args.account:
        return args.account

    return config.get("default_account")


# -----------------------------
# CLI
# -----------------------------
def main():
    config = load_config()

    parser = argparse.ArgumentParser(description="INWX API CLI Tool")

    parser.add_argument(
        "--account",
        required=False,
        help="Select INWX account (overrides default_account in config)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # config subcommand
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_subparsers = config_parser.add_subparsers(dest="config_command", required=True)

    # init
    config_init_parser = config_subparsers.add_parser("init", help="Initialize config file")
    config_init_parser.set_defaults(func=config_init)

    # add
    config_add_parser = config_subparsers.add_parser("add", help="Add new account")
    config_add_parser.set_defaults(func=config_add)

    # remove
    config_remove_parser = config_subparsers.add_parser("remove", help="Remove account")
    config_remove_parser.add_argument("account", help="Account name")
    config_remove_parser.set_defaults(func=config_remove)

    # set-default
    config_set_default_parser = config_subparsers.add_parser("default", help="Set default account")
    config_set_default_parser.add_argument("account", help="Account name")
    config_set_default_parser.set_defaults(func=config_set_default)

    # list
    config_list_parser = config_subparsers.add_parser("list", help="List configured accounts")
    config_list_parser.set_defaults(func=config_list)

    register_methods(subparsers, NAMESERVER_METHODS)
    register_methods(subparsers, DOMAIN_METHODS)

    args = parser.parse_args()

    # Special case: config commands do not need API login
    if args.command == "config":
        args.func(args)
        return

    account = args.account or config.get("default_account")

    if not account:
        print("No account specified and no default_account configured.", file=sys.stderr)
        sys.exit(1)

    user, pwd, secret = get_credentials(config, account)

    if not user or not pwd:
        print(f"Missing credentials for account '{account}'.", file=sys.stderr)
        sys.exit(1)

    ctx = CLIContext(config, account, user, pwd, secret)

    try:
        with ctx as api:
            result = args.func(api, args.api_method, args, ctx)
            print_json(result)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
