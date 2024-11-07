---
hide:
    - toc
---

# GetDatasetMetadata API 

<div class='subtitle'>Get the metadata associated with your Dataset</div>

The GetDatasetMetadata API allows you to get the metadata associated with a dataset in a programmatic way.

---
### `get_dataset_metadata` 

The `get_dataset_metadata method` is used to get the metadata for a dataset from the Invariant API using the `dataset_name`.

##### `request` <span class='type'>dataset_name</span> <span class='required'/>

The name of the dataset.

##### `request_kwargs` <span class='type'>Optional[Dict[str, Any]]</span> <span class='optional'/>

Additional keyword arguments to pass to the requests method. Default is `None`.

##### Return Value

##### <span class='type'>Dict</span>

The response object from the Invariant API.


> Example
    ```python
    from invariant_sdk.client import Client
    from invariant_sdk.types.push_traces import PushTracesRequest

    client = Client()

    dataset_metadata = client.get_dataset_metadata(dataset_name="some_dataset_name")
    ```
