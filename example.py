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

client = Client(api_url="https://preview-explorer.invariantlabs.ai")
client.create_request_and_push_trace(traces, dataset="my-first-dataset")
