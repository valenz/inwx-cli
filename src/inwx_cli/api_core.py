# inwx_cli/api_core.py

import re
from .exceptions import INWXAPIError

CLI_INTERNAL_ARGS = {
    "account",
    "command",
    "func",
    "api_method",
}


def kebab(name: str) -> str:
    return re.sub(r"([a-z])([A-Z])", r"\1-\2", name).lower()


def extract_api_params(args) -> dict:
    params = {}

    for k, v in vars(args).items():
        if k in CLI_INTERNAL_ARGS:
            continue
        if v is None:
            continue
        if isinstance(v, list) and not v:
            continue

        params[k] = v

    return params


def handle_generic(api, api_method, args):
    params = extract_api_params(args)

    result = api.call_api(
        api_method=api_method,
        method_params=params,
    )

    if result.get("code") not in (1000, 1001):
        raise INWXAPIError(result)

    return result


def register_methods(subparsers, methods_dict):
    for method_name, info in methods_dict.items():
        parser = subparsers.add_parser(method_name, help=f"{method_name} API call")

        for param_name, param_info in info.get("params", {}).items():
            flag = "--" + kebab(param_name)
            parser.add_argument(flag, **param_info)

        parser.set_defaults(api_method=method_name, func=handle_generic)
