---
hide:
    - toc
---

# UpdateDatasetMetadata API

<div class='subtitle'>Update the metadata associated with your Dataset</div>

The UpdateDatasetMetadata API allows you to update the metadata for a dataset in a programmatic way.

## Data Types

### `MetadataUpdate`

The `MetadataUpdate` class holds the metadata attributes which you want to update. Only the following fields can be updated:

##### `benchmark` <span class='type'>Optional[str]</span> <span class='optional'/>

The name of the benchmark. Must not be an empty string or a string containing only whitespace.

##### `accuracy` <span class='type'>Optional[Union[float, int]]</span> <span class='optional'/>

The accuracy score. Must not be negative.

##### `name` <span class='type'>Optional[str]</span> <span class='optional'/>

The name of the agent that achieved this accuracy score on the given benchmark. Must not be an empty string or a string containing only whitespace.

If `benchmark=web-arena, accuracy=0.95, name=gpt-4o`: this means that for the gpt-4o agent on the web-arena benchmark we achieved 95% accuracy.

### `UpdateDatasetMetadataRequest`

The `UpdateDatasetMetadataRequest` class holds the request data for updating metadata.


##### `dataset_name` <span class='type'>str</span> <span class='required'/>

The name of the dataset.

##### `replace_all` <span class='type'>bool</span> <span class='optional'/>

When replace_all is False:

1. If an attribute doesn't exist or is set to `None` in `metadata`, it is ignored.

2. For the other attributes in `metadata`, the values are used to update the metadata for the dataset.

When replace_all is True:

1. If an attribute doesn't exist or is set to `None` in `metadata`, the corresponding key is deleted from the dataset metadata.

2. For the other attributes in `metadata`, the values are used to update the metadata for the dataset.

If `replace_all=True` is passed but `metadata` is empty - that deletes all set metadata for the dataset. 

##### `metadata` <span class='type'>MetadataUpdate</span> <span class='optional'/>

The metadata class which contains attributes to update.


## Updating metadata

There are two SDK methods to update metadata: `update_dataset_metadata` and `create_request_and_update_dataset_metadata`. The former accepts the `UpdateDatasetMetadataRequest` type as an argument and the latter accepts Python-native types as arguments.

### `update_dataset_metadata` 
The `update_dataset_metadata` method is used to update the metadata for a dataset.

##### `request` <span class='type'>UpdateDatasetMetadataRequest</span> <span class='required'/>

The request object containing information to update the metadata.

##### `request_kwargs` <span class='type'>Optional[Dict[str, Any]]</span> <span class='optional'/>

Additional keyword arguments to pass to the requests method. Default is `None`.

##### Return Value

##### <span class='type'>Dict</span>

The response object from the Invariant API.


> Example
    ```python
    from invariant_sdk.client import Client
    from invariant_sdk.types.update_dataset_metadata import UpdateDatasetMetadataRequest, MetadataUpdate

    client = Client()

    # Metadata state: {}
    
    request_1 = UpdateDatasetMetadataRequest(
        dataset_name="some_name",
        metadata=MetadataUpdate(benchmark="some_benchmark")
    )
    response_1 = client.update_dataset_metadata(request_1)
    
    # Metadata state: {"benchmark": "some_benchmark"}

    request_2 = UpdateDatasetMetadataRequest(
        dataset_name="some_name",
        metadata=MetadataUpdate(accuracy=5, name="xyz")
    )

    response_2 = client.update_dataset_metadata(request_2)

    # Metadata state: {"benchmark": "some_benchmark", "accuracy": 5, "name": "xyz"}

    request_3 = UpdateDatasetMetadataRequest(
        dataset_name="some_name",
        replace_all=True
        metadata=MetadataUpdate(benchmark="new_benchmark")
    )

    response_3 = client.update_dataset_metadata(request_3)

    # Metadata state: {"benchmark": "new_benchmark"}

    ```

> Example to clear all previously set metadata
    ```python
    from invariant_sdk.client import Client
    from invariant_sdk.types.update_dataset_metadata import UpdateDatasetMetadataRequest, MetadataUpdate

    client = Client()

    request = UpdateDatasetMetadataRequest(
        dataset_name="some_name",
        replace_all=True,
        metadata=MetadataUpdate()
    )

    response = client.update_dataset_metadata(request)
    ```    

### `create_request_and_update_dataset_metadata`

The `create_request_and_update_dataset_metadata` method is used to update the metadata for a dataset.

##### `dataset_name` <span class='type'>str</span> <span class='required'/>

The name of the dataset. 

##### `replace_all` <span class='type'>bool</span> <span class='optional'/>

The `replace_all` field as described above.

##### `metadata` <span class='type'>Optional[Dict]</span> <span class='optional'/>

The dictionary containing the metadata to be used for update. Default is `None`.

##### `request_kwargs` <span class='type'>Optional[Mapping]</span> <span class='optional'/>

Additional keyword arguments to pass to the requests method. Default is `None`.

##### Return Value

##### <span class='type'>Dict</span>

The response object from the Invariant API.

> Example
    ```python
    from invariant_sdk.client import Client

    client = Client()

    # Metadata state: {}
    
    response_1 = client.create_request_and_update_dataset_metadata(
        dataset_name="some_name",
        metadata={"benchmark": "some_benchmark"}
    )
    
    # Metadata state: {"benchmark": "some_benchmark"}

    response_2 = client.create_request_and_update_dataset_metadata(
        dataset_name="some_name",
        metadata={"accuracy": 5, "name": "xyz"}
    )

    # Metadata state: {"benchmark": "some_benchmark", "accuracy": 5, "name": "xyz"}

    response_3 = client.create_request_and_update_dataset_metadata(
        dataset_name="some_name",
        replace_all=True,
        metadata={"benchmark": "new_benchmark"}
    )

    # Metadata state: {"benchmark": "new_benchmark"}
    ```

> Example to clear all previously set metadata
    ```python
    from invariant_sdk.client import Client

    client = Client()

    response = client.create_request_and_update_dataset_metadata(
        dataset_name="some_name"
        replace_all=True,
    )
    ```
