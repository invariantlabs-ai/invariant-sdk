# Invariantlabs Client SDK

This repository contains the Python SDK for interacting with the [Invariantlabs](https://invariantlabs.ai/) APIs.

This documentation will guide you through the process of setting up the SDK, capturing traces, and uploading them to the Invariant Explorer. The SDK currently only supports Python.

## Documentation
Visit [this](https://explorer.invariantlabs.ai/docs/) to see how to use the SDK.

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
