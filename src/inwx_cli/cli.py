# inwx_cli/cli.py

import sys
import json
import argparse
from .config import (
    config_init,
    config_add,
    config_remove,
    config_set_default,
    config_list,
    config_doctor,)
from .config import load_config
from .context import CLIContext
from .exceptions import INWXAPIError
from .api_core import register_methods
from .api_methods.nameserver import METHODS as NAMESERVER_METHODS
from .api_methods.domain import METHODS as DOMAIN_METHODS


# -----------------------------
# Helpers
# -----------------------------
def get_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def get_username(config, account):
    if account in config:
        return config[account].get("username")
    return None


def exit_with(rc: int | None):
    if rc is None:
        sys.exit(0)
    sys.exit(rc)


# -----------------------------
# CLI
# -----------------------------
def main():
    config = load_config(check_permissions=True)

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
    config_remove_parser = config_subparsers.add_parser("del", help="Remove account")
    config_remove_parser.add_argument("account", help="Account name")
    config_remove_parser.set_defaults(func=config_remove)

    # set-default
    config_set_default_parser = config_subparsers.add_parser("default", help="Set default account")
    config_set_default_parser.add_argument("account", help="Account name")
    config_set_default_parser.set_defaults(func=config_set_default)

    # list
    config_list_parser = config_subparsers.add_parser("list", help="List configured accounts")
    config_list_parser.set_defaults(func=config_list)

    # doctor
    config_doctor_parser = config_subparsers.add_parser("doctor", help="Check config and keyring consistency")
    config_doctor_parser.set_defaults(func=config_doctor)

    register_methods(subparsers, NAMESERVER_METHODS)
    register_methods(subparsers, DOMAIN_METHODS)

    args = parser.parse_args()

    # Special case: config commands do not need API login
    if args.command == "config":
        rc = args.func(args)
        exit_with(rc)

    account = args.account or config.get("default_account")

    if not account:
        print("No account specified and no default_account configured.", file=sys.stderr)
        exit_with(1)

    username = get_username(config, account)

    if not username:
        print(f"Missing credentials for account '{account}'.", file=sys.stderr)
        exit_with(1)

    ctx = CLIContext(config, account, username)

    try:
        with ctx as api:
            result = args.func(api, args.api_method, args)
            print(get_json(result))
            rc = 0

    except INWXAPIError as e:
        print(get_json(e.result), file=sys.stderr)
        rc = 2

    except Exception as e:
        print(e, file=sys.stderr)
        rc = 3

    exit_with(rc)


if __name__ == "__main__":
    main()
