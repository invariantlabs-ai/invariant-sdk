# Welcome to Invariant

<div class='subtitle'>Getting started with the Invariant SDK</div>

The Invariant SDK enables you to share, analyze and collaborate on AI agent runtime traces. This documentation will guide you through the process of setting up the SDK, capturing traces, and uploading them to the Invariant Explorer. The SDK currently only supports Python.

## Install via pip directly
```bash
pip install git+https://github.com/invariantlabs-ai/invariant-sdk.git#egg=invariant_sdk&subdirectory=python
```

## Include via requirements.txt
You can include the Invariant SDK in your `requirements.txt` file by adding the following line:

```
git+https://github.com/invariantlabs-ai/invariant-sdk.git#egg=invariant_sdk&subdirectory=python
```

## Include via pyproject.toml
To include the Invariant SDK in your `pyproject.toml` file, follow these steps:

### Using `poetry`
1. Add the following line under the `[tool.poetry.dependencies]` section in `pyproject.toml`:

```toml
invariant_sdk = { git = "https://github.com/invariantlabs-ai/invariant-sdk.git", subdirectory = "python" }
```

2. Run the following command to install the dependencies:

```bash
poetry install
```

### Using `hatch`
1. Add the following line under the `dependencies` section in `pyproject.toml`:

```toml
invariant_sdk = { url = "git+https://github.com/invariantlabs-ai/invariant-sdk.git#egg=invariant_sdk&subdirectory=python" }
```

2. Run the following command to install the dependencies:

```bash
hatch env update
```

## Include directly via PyPi
Coming soon!