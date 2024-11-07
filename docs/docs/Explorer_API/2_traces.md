# Trace Format

The Explorer supports agent traces made up of sequences of events like messages, tool calls and environment outputs. The required format is compatible with the [OpenAI chat data structure](https://platform.openai.com/docs/api-reference/chat/create) with [function calling](https://platform.openai.com/docs/guides/function-calling) support.

This documents shows pseudo-code based class definitions to specify the format more formally, but trace data is expected to be JSON serialized.

### `Event`

```python
class Event:
    role: str
    content: Optional[str]
    tool_calls: Optional[list[ToolCall]]
```

##### `role` <span class='type'>string</span> <span class='required'/>

The role of the event, e.g., `user`, `assistant`, `system` or something else.

##### `content` <span class='type'>string</span> <span class='optional'/>

The content of the event, e.g., agent reasoning and intermediate results.

##### `tool_calls` <span class='type'>list[ToolCall]</span> <span class='optional'/>

A list of tool calls made by the agent in this event.


> Examples <br/><br/>
    Simple Message
    ```json
    { "role": "user", "content": "Hello, how are you?" }
    ```
    Message with Tool Call
    ```json
    { 
        "role": "assistant", 
        "content": "Checking your inbox...", 
        "tool_calls": [
            { 
                "id": "1", 
                "type": "function", 
                "function": { 
                    "name": "get_inbox", 
                    "arguments": {
                        "n": 10
                    }
                }
            }
        ]
    }
    ```

### `ToolCall`

```python
class ToolCall:
    id: str
    type: str
    function: Function

class Function:
    name: str
    arguments: dict
```

<!-- * `id (str)`: A unique identifier for the tool call.
* `type (str)`: The type of the tool call, e.g., `function`.
* `function (Function)`: The function call made by the agent.
    * `name (str)`: The name of the function called.
    * `arguments (Dict[str, Any])`: The arguments passed to the function, encoded as a JSON dictionary. -->

##### `id` <span class='type'>string</span> <span class='required'/>

A unique identifier for the tool call.

##### `type` <span class='type'>string</span> <span class='required'/>

The type of the tool call, e.g., `function`.

##### `function` <span class='type'>Function</span> <span class='required'/>

The function call made by the agent.

* ##### `name` <span class='type'>string</span> <span class='required'/>

    The name of the function called.

* ##### `arguments` <span class='type'>dict</span> <span class='required'/>

    The arguments passed to the function, encoded as a JSON dictionary.

> Example
    ```json
    {
        "id": "1",
        "type": "function",
        "function": {
            "name": "get_inbox",
            "arguments": {
                "n": 10
            }
        }
    }
    ```

### `ToolOutput`

A special event type for tool outputs, associated with a previous `ToolCall`.

```python
class ToolOutput(Event):
    role: str
    content: str
    tool_call_id: Optional[str]
```

##### `role` <span class='type'>string</span> <span class='required'/>

The role of the event, e.g., `tool`.

##### `content` <span class='type'>string</span> <span class='required'/>

The content of the tool output, e.g., the result of a function call.

##### `tool_call_id` <span class='type'>string</span> <span class='optional'/>

The identifier of a previous ToolCall that this output corresponds to.

> Example
    ```json
    {
        "role": "tool",
        "tool_call_id": "1",
        "content": "1. Subject: Hello, From: Alice, Date: 2024-01-01, 2. Subject: Meeting, From: Bob, Date: 2024-01-02"
    }
    ```

### Full Trace Example

The format suitable for the Invariant SDK is a list of `Event` objects. Here is an example of a trace with a user asking for their inbox, the assistant fetching the inbox, and the assistant listing the inbox contents.

```json
[
    {
        "role": "user", 
        "content": "What's in my inbox?"
    }, 
    {
        "role": "assistant",
        "content": "Here are the latest emails.", 
        "tool_calls": [
            {
                "id": "1",
                "type": "function",
                "function": {
                    "name": "get_inbox",
                    "arguments": {}
                }
            }
        ]
    },
    {
        "role": "tool",
        "tool_call_id": "1",
        "content": "1. Subject: Hello, From: Alice, Date: 2024-01-0, 2. Subject: Meeting, From: Bob, Date: 2024-01-02"
    },
    {
        "role": "assistant",
        "content": "You have 2 new emails."
    }
]
```