# INWX CLI

A command-line interface (CLI) for interacting with the INWX API, built on top of inwx-domrobot.

This tool allows you to manage domains, nameservers, and related resources directly from the command line in a clean, scriptable, and production-ready way.

---

## Features

- Full-featured CLI wrapper for the INWX DomRobot API
- Domain management (create, delete, renew, transfer, list, etc.)
- Nameserver and DNS record management
- Dynamic mapping of CLI arguments to API parameters
- Multiple account support
- Secure credential storage via system keyring
- Script- and CI-friendly (deterministic JSON output & exit codes)
- Modern Python packaging (PEP 517 / PEP 621, `src/` layout)

---

## Requirements

- Python 3.11+
- An active INWX account
- Internet access to the INWX API

---

## Installation

### Install directly from GitHub (recommended)

No local build steps required:

```bash
pip install git+https://github.com/valenz/inwx-cli.git
```

After installation, the CLI is available as:

```bash
inwx-cli --help
```

---

### Optional: Install with pipx (isolated CLI install)

```bash
pipx install git+https://github.com/valenz/inwx-cli.git
```

This installs `inwx-cli` globally while keeping it isolated from your system Python.

---

## Usage

### Show help

```bash
inwx-cli --help
```

---

### Global options

```bash
inwx-cli --account &lt;account_name&gt; &lt;command&gt; [options]
```

- `--account`  
  Selects an INWX account (overrides `default_account` from the configuration).

If no account is specified, the configured default account is used.

---

## Command Overview

### Configuration

```bash
inwx-cli config &lt;command&gt;
```

Available subcommands:

- `config init` – initialize configuration and store credentials
- `config add` – add a new account
- `config del` – remove an account
- `config list` – list configured accounts
- `config default` – set the default account
- `config doctor` – validate config and keyring consistency

Example workflow:

```bash
inwx-cli config init
inwx-cli config add
inwx-cli config list
inwx-cli config default my-account
```

---

### Nameserver / DNS

```bash
inwx-cli nameserver.&lt;action&gt; [options]
```

Examples:

```bash
inwx-cli nameserver.list
inwx-cli nameserver.info --domain example.com
```

```bash
inwx-cli nameserver.createRecord \
  --domain example.com \
  --type A \
  --name www \
  --content 1.2.3.4
```

```bash
inwx-cli nameserver.deleteRecord --id 123456
```

---

### Domains

```bash
inwx-cli domain.&lt;action&gt; [options]
```

Examples:

```bash
inwx-cli domain.list
inwx-cli domain.info --domain example.com
```

```bash
inwx-cli domain.create --domain example.com --registrant 12345
```

```bash
inwx-cli domain.renew --domain example.com --period 1 --expiration 2025-01-01
```

```bash
inwx-cli domain.delete --domain example.com
```

---

## Boolean Parameters

Some API parameters require explicit boolean values.

### Explicit boolean values

```bash
--no-delegation true
--no-delegation false
```

Accepted values:

```bash
true | false | yes | no | 1 | 0 | on | off | t | f
```

### Boolean flags

```bash
--testing
--transfer-lock
--no-transfer-lock
```

The exact behavior depends on the underlying API method.

---

## Output & Exit Codes

### Output

- Successful commands print **JSON** to `stdout`
- Errors print **JSON** (API errors) or text (internal errors) to `stderr`

Example:

```bash
inwx-cli domain.list &gt; domains.json
```

---

### Exit Codes

| Code | Meaning                                 |
|------|-----------------------------------------|
| `0`  | Success                                 |
| `1`  | Invalid input or configuration problem  |
| `2`  | API error (INWX returned an error code) |
| `3`  | Unexpected internal error               |

---

## Configuration & Security

- Configuration file location:

```bash
~/.config/inwx/config.toml
```

- File permissions are enforced (`600`)
- Passwords and shared secrets are stored securely using the system keyring
- No credentials are written to disk in plain text

---

## Development

### Clone the repository

```bash
git clone https://github.com/valenz/inwx-cli.git
cd inwx-cli
```

---

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### Build and install locally

```bash
python -m pip install --upgrade pip build
python -m build
python -m pip install dist/*.whl
```

---

## Project Structure

```bash
inwx-cli/
├── pyproject.toml
├── README.md
├── LICENSE
└── src/
    └── inwx_cli/
        ├── cli.py
        ├── api_core.py
        ├── api_session.py
        ├── config.py
        ├── context.py
        ├── exceptions.py
        ├── secrets.py
        └── api_methods/
```

CLI entry point:

```bash
[project.scripts]
inwx-cli = "inwx_cli.cli:main"
```

---

## Design Notes

- Generic API wrapper driven by declarative method definitions
- No hardcoded API calls in the CLI layer
- Clear separation between CLI, API logic, and configuration
- Designed for extension without changing core CLI code

---

## License

MIT License — see the LICENSE file for details.

---

## Disclaimer

This project is not officially affiliated with INWX.
