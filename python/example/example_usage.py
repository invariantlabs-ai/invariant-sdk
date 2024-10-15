"""Example usage of the Invariant Python client."""

from invariant.client import Client
from invariant.types.push_traces import PushTracesRequest
from invariant.types.annotations import AnnotationCreate

if __name__ == "__main__":
    client = Client(
        api_url="http://localhost:8000",
        # Add the API key here.
        api_key="",
    )
    push_traces_request = PushTracesRequest(
        messages=[
            [
                {"role": "user", "content": "one"},
                {"role": "assistant", "content": "two \n three"},
            ],
            [
                {"role": "user", "content": "four"},
                {"role": "assistant", "content": "five \n six"},
            ],
        ],
        annotations=[
            [
                AnnotationCreate(
                    content="annotating one",
                    address="messages[0].content:L0",
                    extra_metadata={"key1": "value1"},
                ),
                AnnotationCreate(
                    content="annotating two",
                    address="messages[1].content:L0",
                    extra_metadata={"key1": "value1"},
                ),
                AnnotationCreate(
                    content="annotating two again",
                    address="messages[1].content:L0",
                    extra_metadata={"key1": "value1"},
                ),
                AnnotationCreate(
                    content="annotating three",
                    address="messages[1].content:L1",
                    extra_metadata={"key1": "value1"},
                ),
            ],
            [
                AnnotationCreate(
                    content="annotating four",
                    address="messages[0].content:L0",
                    extra_metadata={"key1": "value1"},
                ),
                AnnotationCreate(
                    content="annotating five",
                    address="messages[1].content:L0",
                    extra_metadata={"key1": "value1"},
                ),
                AnnotationCreate(
                    content="annotating six",
                    address="messages[1].content:L1",
                    extra_metadata={"key1": "value1"},
                ),
                AnnotationCreate(
                    content="annotating six again",
                    address="messages[1].content:L1",
                    extra_metadata={"key1": "value1"},
                ),
            ],
        ],
    )
    response = client.push_trace(push_traces_request)
    print(response)
