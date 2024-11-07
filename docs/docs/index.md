---
title: Getting Started
---

# Getting Started With Explorer

<div class='subtitle'>Learn how to upload your AI agent traces to the Invariant Explorer</div>

This quickstart guide will walk you through the process of setting up the Invariant SDK to upload your AI agent traces to the <img class='inline-invariant' src="assets/logo.svg"/> [Invariant Explorer](https://explorer.invariantlabs.ai). 

You can use Explorer to visualize, analyze, and collaborate on your AI agent traces, as well as compare them with other agents and models.

## 1. Create an Explorer Account

First, navigate to the <img class='inline-invariant' src="assets/logo.svg"/> [Invariant Explorer](https://explorer.invariantlabs.ai) and create an account via GitHub Sign-In.

Once you have created an account, go to your [User Settings](https://explorer.invariantlabs.ai/settings) and generate an API key.

Make note of your API key, as you will need it to authenticate your uploads. If you're running in a shell, you can export the API key now as an environment variable:

```bash
export INVARIANT_API_KEY=<your-api-key>
```

## 2. Install the Invariant SDK

Next, install the Invariant SDK in your Python environment, by running the following command. See [Installation](installation.md) for alternative methods using different package managers.

```bash
pip install invariant-sdk
```

## 3. Prepare Your Traces and Upload

Now, you can start preparing your AI agent traces for upload. The Invariant SDK then provides a `Client` class that you can use to upload your traces in an Invariant-compatible format:

```python
from invariant_sdk.client import Client

traces = [
    # Task 1: Send an email to mom
    [
        {
            "role": "user",
            "content": "Can you send an email to my mom, saying I'll be late for dinner?",
        },
        {
            "role": "assistant",
            "content": "Sending an email to your mom now.",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {
                        "name": "send_email",
                        "arguments": {
                            "to": "mom@mail.com",
                            "subject": "Running late, sorry!",
                        }
                    }
                }
            ]
        }
    ]
]

client = Client()
client.create_request_and_push_trace(traces, dataset="my-first-dataset")
```

This will upload your traces to the Invariant Explorer under a new dataset named `my-first-dataset`. If the corresponding dataset already exists, the traces will be appended to it.

To learn more about the expected trace format see the chapter on the [trace format requirements](Explorer_API/2_traces.md).

## Work With Your Traces in Explorer

You can now navigate to the following URL to view your uploaded traces:

```
https://explorer.invariantlabs.ai/<your_username>/my-first-dataset/t/1
```

You can also use the Invariant Explorer to analyze your traces, compare them with other agents, and collaborate with your team.

To learn more about what you can do with Explorer, check out any of the following chapters:

<div class='tiles'>

<a href="benchmarks.html" class='tile'>
    <span class='tile-title'>Benchmarks →</span>
    <span class='tile-description'>Submit your AI agent to the Invariant benchmark registry for comparison</span>
</a>

<a href="Explorer_API/2_traces.html" class='tile'>
    <span class='tile-title'>Trace Format →</span>
    <span class='tile-description'>Learn about the Invariant trace format and how to structure your traces for ingestion</span>
</a>

<a href="Explorer_API/1_client_setup.html" class='tile'>
    <span class='tile-title'>Client Setup →</span>
    <span class='tile-description'>Setting up endpoints and authentication for the Invariant SDK</span>
</a>

<a href="Explorer_API/Uploading_Traces/push_api.html" class='tile'>
    <span class='tile-title'>Pushing Traces →</span>
    <span class='tile-description'>Learn about traces, datasets and annotations.</span>
</a>

</div>
