# Client Setup

The SDK exposes a `Client` class. To create an object of this type, you need two variables: the Invariant API endpoint URL and the API key.
The Invariant API endpoint URL is `https://explorer.invariantlabs.ai`.

## Getting the API Key
1. Go to [https://explorer.invariantlabs.ai/settings](https://explorer.invariantlabs.ai/settings).
2. Click on `New API Key`.
3. Click on the API Key to copy it. Save this somewhere, as you won't be able to view the key again once you close the modal.

## Setting Up Environment Variables
```bash
export INVARIANT_API_ENDPOINT=https://explorer.invariantlabs.ai
# Add the API key here.
export INVARIANT_API_KEY=YourAPIKey
```

## Creating a Client
This will use the environment variables to set the Invariant API endpoint URL and the API key values.
```python
from invariant_sdk.client import Client

client = Client()
```

## Creating a Client to Override Environment Variables
This will override the environment variables.

```python
from invariant_sdk.client import Client

client = Client(
    api_url="https://explorer.invariantlabs.ai",
    # Add the API key here.
    api_key="YourAPIKey",
)
```