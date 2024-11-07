---
hide:
    - toc
---

# Push API

<div class='subtitle'>Upload your agent traces via the Push API</div>

The Push API allows you to upload your agent traces to your Explorer account in a programmatic way.

## Data Types

### `PushTracesRequest`

The `PushTracesRequest` class holds the request data for a trace upload request.

<!-- - **messages** (`List[List[Dict]]`): The messages to push to the Invariant API.
- **annotations** (`Optional[List[List[AnnotationCreate]]]`): The annotations to push to the Invariant API. Default is `None`.
- **dataset** (`Optional[str]`): The dataset name. Default is `None`.
- **metadata** (`Optional[List[Dict]]`): The metadata to push to the Invariant API. Default is `None`. -->

##### `messages` <span class='type'>List[List[Dict]]</span> <span class='required'/>

The list of messages or events to be uploaded. 

Must be in the [required trace format](../2_traces.md). Must not be empty.

##### `annotations` <span class='type'>Optional[List[List[AnnotationCreate]]</span> <span class='optional'/>

The annotations to push to the Invariant API. 

Must be the same length as messages if provided. Must be a list of lists of `AnnotationCreate` type if provided.

##### `dataset` <span class='type'>Optional[str]</span> <span class='optional'/>

The dataset name. 

If `None`, the traces are uploaded as snippets (traces not attached to any dataset).

If you specify a dataset which doesn't exist, a new dataset is created.

##### `metadata` <span class='type'>Optional[List[Dict]]</span> <span class='optional'/>

The metadata to attach to each uploaded trace.

Must be a list of dictionaries if provided and must be the same length as messages if provided.

Each metadata dictionary can have arbitrary keys and values for storing additional information about the trace.

See [File Uploads](../Uploading_Traces/file_uploads.md) for more information on metadata.

### `AnnotationCreate`

The `AnnotationCreate` class holds the data for an annotation to be created.

See [Annotations](../3_annotations.md) for more information on annotations.

##### `content` <span class='type'>str</span> <span class='required'/>

The content of the annotation.

##### `address` <span class='type'>str</span> <span class='required'/>

The address of the annotation.

##### `extra_metadata` <span class='type'>Optional[Dict[Any, Any]]</span> <span class='optional'/>

Additional metadata for the annotation.

Each metadata dictionary can have arbitrary keys and values for storing additional information about the annotation.

### `PushTracesResponse`

The `PushTracesResponse` class holds the response data from the PushTraces API.

##### `id` <span class='type'>List[str]</span> <span class='required'/>

The list of IDs for the created traces.

##### `dataset` <span class='type'>Optional[str]</span> <span class='optional'/>

The dataset name. Default is `None`.


## Pushing Traces

There are two SDK methods to push traces: `push_trace` and `create_request_and_push_trace`. The former accepts the `PushTracesRequest` type as an argument and the latter accepts Python-native types as arguments.

### `push_trace` 
The `push_trace` method is used to push trace data to the Invariant API using a pre-constructed request object.

##### `request` <span class='type'>PushTracesRequest</span> <span class='required'/>

The request object containing trace data.

##### `request_kwargs` <span class='type'>Optional[Dict[str, Any]]</span> <span class='optional'/>

Additional keyword arguments to pass to the requests method. Default is `None`.

##### Return Value

##### <span class='type'>PushTracesResponse</span>

The response object from the Invariant API.


> Example
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

##### `messages` <span class='type'>List[List[Dict]]</span> <span class='required'/>

The messages to push to the Invariant API.

##### `annotations` <span class='type'>Optional[List[List[Dict]]</span> <span class='optional'/>

The annotations to push to the Invariant API. Default is `None`.

##### `metadata` <span class='type'>Optional[List[Dict]]</span> <span class='optional'/>

The metadata to push to the Invariant API. Default is `None`.

##### `dataset` <span class='type'>Optional[str]</span> <span class='optional'/>

The dataset name. Default is `None`. If `None`, the traces are uploaded as snippets which are not attached to any dataset. If you specify a dataset which doesn't exist, then the API creates the dataset.

##### `request_kwargs` <span class='type'>Optional[Mapping]</span> <span class='optional'/>

Additional keyword arguments to pass to the requests method. Default is `None`.

##### Return Value

##### <span class='type'>PushTracesResponse</span>

The response object from the Invariant API.

> Example
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