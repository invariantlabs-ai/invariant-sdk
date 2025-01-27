"""Example usage of the Invariant Python client."""

from invariant_sdk.client import Client

if __name__ == "__main__":
    client = Client(
        api_url="http://127.0.0.1",
        # Add the API key here.
        api_key="",
    )
    messages = [
        [
            {"role": "user", "content": "one"},
            {"role": "assistant", "content": "two \n three"},
        ],
        [
            {"role": "user", "content": "four"},
            {"role": "assistant", "content": "five \n six"},
        ],
    ]
    annotations = [
        [
            {
                "content": "annotating one",
                "address": "messages[0].content:L0",
                "extra_metadata": {"key1": "value1"},
            },
            {
                "content": "annotating two",
                "address": "messages[1].content:L0",
                "extra_metadata": {"key2": "value2"},
            },
            {
                "content": "annotating two again",
                "address": "messages[1].content:L0",
                "extra_metadata": {"key3": "value3"},
            },
            {
                "content": "annotating three",
                "address": "messages[1].content:L1",
                "extra_metadata": {"key4": "value4"},
            },
        ],
        [
            {
                "content": "annotating four",
                "address": "messages[0].content:L0",
                "extra_metadata": {"key5": "value5"},
            },
            {
                "content": "annotating five",
                "address": "messages[1].content:L0",
                "extra_metadata": {"key6": "value6"},
            },
            {
                "content": "annotating six",
                "address": "messages[1].content:L1",
                "extra_metadata": {"key7": "value7"},
            },
            {
                "content": "annotating six again",
                "address": "messages[1].content:L1",
                "extra_metadata": {"key8": "value8"},
            },
        ],
    ]
    metadata = [{"meta_key_1": "meta_value_1"}, {"meta_key_2": "meta_value_2"}]
    response = client.create_request_and_push_trace(
        messages=messages, annotations=annotations, metadata=metadata
    )
    print(response)
