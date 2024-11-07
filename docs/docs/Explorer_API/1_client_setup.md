# Client Setup

The SDK exposes a `Client` class. To create an object of this type, you need two variables: the Invariant API endpoint URL and the API key.

## Getting the API Key
Navigate to the <img class='inline-invariant' src="../assets/logo.svg"/> [Invariant Explorer](https://explorer.invariantlabs.ai) and create an account via GitHub Sign-In.

Once you have created an account, go to your [User Settings](https://explorer.invariantlabs.ai/settings) and generate an API key.

Make note of your API key, as you will need it to authenticate your uploads. If you're running in a shell, you can export the API key now as an environment variable:

## Setting Up Environment Variables

Navigate to your shell and export the API key as an environment variable. You can optionally set the API endpoint URL as an environment variable as well, which allows you to use private instances of Explorer.

```bash
export INVARIANT_API_ENDPOINT=https://explorer.invariantlabs.ai
# Add the API key here.
export INVARIANT_API_KEY=YourAPIKey
```

## Creating a Client

In your Python code, you can create a `Client` object. This object will use the environment variables you set up earlier to authenticate your uploads.

```python
from invariant_sdk.client import Client

client = Client()
```

Without parameters, the `Client` object will automatically use the environment variables you set up earlier and the default Explorer instance at `https://explorer.invariantlabs.ai`.

## Overriding Environment Configuration

If you want to override the environment configuration or use a different API key, you can also pass the API endpoint URL and API key as arguments to the `Client` constructor directly.

```python
from invariant_sdk.client import Client

client = Client(
    api_url="https://explorer.invariantlabs.ai",
    # Add the API key here.
    api_key="YourAPIKey",
)
```