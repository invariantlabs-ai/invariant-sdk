# Installation

<div class='subtitle'>Installing the Invariant SDK for Python</div>

The Invariant SDK enables you to share, analyze and collaborate on AI agent runtime traces. This documentation will guide you through the process of setting up the SDK, capturing traces, and uploading them to the Invariant Explorer. The SDK currently only supports Python.

## Install via pip directly
```bash
pip install invariant-sdk
```

## Include via requirements.txt
You can include the Invariant SDK in your `requirements.txt` file by adding `invariant-sdk`.

## Include via pyproject.toml
To include the Invariant SDK in your `pyproject.toml` file, follow these steps:

### Using `poetry`
1. Add `invariant-sdk` under the `[tool.poetry.dependencies]` section in `pyproject.toml`.

2. Run the following command to install the dependencies:
```
poetry install
```

### Using `hatch`
1. Add `invariant-sdk` under the `dependencies` section in `pyproject.toml`.

2. Run the following command to install the dependencies:
```bash
hatch env update
```
