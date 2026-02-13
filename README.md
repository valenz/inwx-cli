# INWX CLI

A command-line interface (CLI) for interacting with the INWX API, built on top of inwx-domrobot.

This tool allows you to manage domains, nameservers, and related resources directly from the command line in a clean, scriptable, and production-ready way.

## Features

- Full-featured CLI for the INWX API
- Domain management (create, delete, renew, transfer, list, etc.)
- Nameserver and DNS record management
- Multiple account support
- Safe configuration handling
- Designed for automation and DevOps workflows
- Modern Python packaging (PEP 517 / PEP 621)

## Requirements

- Python 3.11+
- An active INWX account
- Internet access to the INWX API

## Installation
### Install directly from GitHub (recommended)

No local build steps required.
```
pip install git+https://github.com/valenz/inwx-cli.git
```

After installation, the CLI is available as:
```
inwx-cli --help
```

### Optional: Install with pipx (isolated CLI install)
```
pipx install git+https://github.com/valenz/inwx-cli.git
```

This installs inwx-cli globally while keeping it isolated from your system Python.

## Usage
### Show help
```
inwx-cli --help
```

### Global options
```
inwx-cli --account <account_name> <command> [options]
```

- `--account`
Selects an INWX account (overrides the default account in the configuration).

## Command Overview
### Configuration
```
inwx-cli config <command>
```

Available subcommands include:

- config init
- config add
- config list
- config set-default
- config remove

### Nameserver
```
inwx-cli nameserver.<action> [options]
```

Examples:
```
inwx-cli nameserver.list
inwx-cli nameserver.info --domain example.com
inwx-cli nameserver.createRecord --domain example.com --type A --name www --content 1.2.3.4
inwx-cli nameserver.deleteRecord --id 123456
```

### Domains
```
inwx-cli domain.<action> [options]
```

Examples:
```
inwx-cli domain.list
inwx-cli domain.info --domain example.com
inwx-cli domain.create --domain example.com --period 1
inwx-cli domain.renew --domain example.com
inwx-cli domain.delete --domain example.com
```

## Configuration

The CLI stores its configuration locally and supports multiple accounts.

Typical workflow:
```
inwx-cli config init
inwx-cli config add
inwx-cli config list
inwx-cli config set-default
```

Credentials are stored locally and are never committed to the repository.

### Development
### Clone the repository
```
git clone https://github.com/valenz/inwx-cli.git
cd inwx-cli
```

### Create a virtual environment
```
python -m venv .venv
source .venv/bin/activate
```

### Build and install locally
```
python -m pip install --upgrade pip build
python -m build
python -m pip install dist/*.whl
```

## Project Structure
```
inwx-cli/
├── pyproject.toml
├── README.md
├── LICENSE
└── src/
    └── inwx_cli/
```

The CLI entry point is defined via:
```
[project.scripts]
inwx-cli = "inwx_cli.cli:main"
```

## Design Notes

- Uses a dedicated top-level package (inwx_cli) to avoid namespace collisions
- Built with the src/ layout
- Uses relative imports internally
- Safe to use alongside other INWX-related Python packages

## License

MIT License — see the LICENSE file for details.

## Disclaimer

This project is not officially affiliated with INWX.
