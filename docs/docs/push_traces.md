# Push Traces

<div class='subtitle'>Pushing traces to Invariant</div>

## Model classes

### `PushTracesRequest`

The `PushTracesRequest` class is a model that holds the request data for the PushTraces API.

#### Attributes
- **messages** (`List[List[Dict]]`): The messages to push to the Invariant API.
- **annotations** (`Optional[List[List[AnnotationCreate]]]`): The annotations to push to the Invariant API. Default is `None`.
- **dataset** (`Optional[str]`): The dataset name. Default is `None`.
- **metadata** (`Optional[List[Dict]]`): The metadata to push to the Invariant API. Default is `None`.

#### Field Validations
**messages**

* Must be a list of lists of dictionaries.
* Cannot be empty.

**annotations**

* Must be the same length as messages if provided.
* Must be a list of lists of `AnnotationCreate` type if provided.

**metadata**

* Must be the same length as messages if provided.
* Must be a list of dictionaries if provided.

### `AnnotationCreate`

The `AnnotationCreate` class is a model that holds the annotation data for Create APIs.

#### Attributes
- **content** (`str`): The content of the annotation.
- **address** (`str`): The address of the annotation.
- **extra_metadata** (`Optional[Dict[Any, Any]]`): Additional metadata for the annotation. Default is `None`.

### `PushTracesResponse`

The `PushTracesResponse` class is a model that holds the response data from the PushTraces API.

#### Attributes
- **id** (`List[str]`): The list of IDs returned by the Invariant API.
- **dataset** (`Optional[str]`): The dataset name. Default is `None`.

## API

There are two methods to push traces: `push_trace` and `create_request_and_push_trace`. The former accepts the `PushTracesRequest` type as an argument and the latter accepts Python native types as arguments.

### `push_trace`
The `push_trace method` is used to push trace data to the Invariant API using a pre-constructed request object.

### Parameters
- **request**  (PushTracesRequest): The request object containing trace data.
- **request_kwargs** (Optional[Mapping]): Additional keyword arguments to pass to the requests method. Default is None.

### Returns
- **PushTracesResponse**: The response object from the Invariant API.

## Example Usage
```python
from invariant_sdk.client import Client
from invariant_sdk.types.push_traces import PushTracesRequest

client = Client()

request = PushTracesRequest(
    messages=[
        [
            {"role": "user", "content": "one"},
            {"role": "assistant", "content": "two \n three"},
        ]
    ],
    annotations=[
        [
            {
                "content": "annotating one",
                "address": "messages[0].content:L0",
                "extra_metadata": {"key1": "value1"},
            }
        ]
    ],
    metadata=[{"meta_key_1": "meta_value_1"}],
    dataset="dataset_name"
)

response = client.push_trace(request)
```

### `create_request_and_push_trace`

The `create_request_and_push_trace` method is used to push trace data to the Invariant API. It creates a request object from the provided messages, annotations, and metadata, and then pushes this data to the API.

### Parameters
- **messages** (`List[List[Dict]]`): The messages to push to the Invariant API.
- **annotations** (`Optional[List[List[Dict]]]`): The annotations to push to the Invariant API. Default is `None`.
- **metadata** (`Optional[List[Dict]]]`): The metadata to push to the Invariant API. Default is `None`.
- **dataset** (`Optional[str]`): The dataset name. Default is `None`. if `None`, the traces are uploaded as snippets which are not attached to any dataset. If you specify a dataset which doesn't exist, then the API creates the dataset.
- **request_kwargs** (`Optional[Mapping]`): Additional keyword arguments to pass to the requests method. Default is `None`.

### Returns
- **PushTracesResponse**: The response object from the Invariant API.

### Example Usage
```python
from invariant_sdk.client import Client

client = Client()

messages = [
    [
        {"role": "user", "content": "one"},
        {"role": "assistant", "content": "two \n three"},
    ]
]

annotations = [
    [
        {
            "content": "annotating one",
            "address": "messages[0].content:L0",
            "extra_metadata": {"key1": "value1"},
        }
    ]
]

metadata = [{"meta_key_1": "meta_value_1"}]

response = client.create_request_and_push_trace(
    messages=messages,
    annotations=annotations,
    metadata=metadata,
    dataset="dataset_name"
)
```
