# inwx_cli/api_core.py

def handle_generic(api, api_method, args, ctx=None):
    """
    Generic INWX API call handler.

    :param ctx: runtime context object
    :param api: INWX API session object
    :param api_method: API method string, e.g. 'domain.create'
    :param args: argparse.Namespace with CLI arguments
    """

    params = {
        k: v for k, v in vars(args).items()
        if v is not None and k not in ("account", "command", "func", "api_method")
    }

    result = api.call_api(api_method=api_method, method_params=params)

    if result.get("code") not in (1000, 1001):
        raise Exception(result)

    return result


def register_methods(subparsers, methods_dict):
    """
    Register API methods dynamically in CLI.

    :param subparsers: argparse subparsers object
    :param methods_dict: dictionary containing API method definitions
    """

    for method_name, info in methods_dict.items():
        parser = subparsers.add_parser(method_name, help=f"{method_name} API call")

        for param_name, param_info in info.get("params", {}).items():
            parser.add_argument(f"--{param_name}", **param_info)

        parser.set_defaults(api_method=method_name, func=handle_generic)
