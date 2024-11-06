# Trace Format

The Invariant stack works with agent traces that are sequences of events like messages, tool calls and environment outputs. 

The required format is largely based on the [OpenAI chat data structures](https://platform.openai.com/docs/api-reference/chat/create) with [function calling](https://platform.openai.com/docs/guides/function-calling).

This documents shows pseudo-code based class definitions to illustrate, but trace data is expected to be in JSON format.

### `Event`

```python
class Event:
    role: str
    content: Optional[str]
    tool_calls: Optional[list[ToolCall]]
```

* `role (str)`: The role of the event, e.g., `user`, `assistant`, `system` or something else.

* `content (str)`: The content of the event, e.g., agent reasoning and intermediate results.

* `tool_calls (Optional[List[ToolCall]])`: A list of tool calls made by the agent at this point in time.


> Example
    ```json
    { "role": "user", "content": "Hello, how are you?" }
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

* `id (str)`: A unique identifier for the tool call.
* `type (str)`: The type of the tool call, e.g., `function`.
* `function (Function)`: The function call made by the agent.
    * `name (str)`: The name of the function called.
    * `arguments (Dict[str, Any])`: The arguments passed to the function, encoded as a JSON dictionary.

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

```python
class ToolOutput(Event):
    role: str
    content: str
    tool_call_id: Optional[str]
```

* `role (str)`: The role of the event, e.g., `tool`.
* `content (str)`: The content of the tool output, e.g., the result of a function call.
* `tool_call_id (Optional[str])`: The identifier of a previous ToolCall that this output corresponds to.

> Example
    ```json
    {
        "role": "tool",
        "tool_call_id": "1",
        "content": "1. Subject: Hello, From: Alice, Date: 2024-01-01, 2. Subject: Meeting, From: Bob, Date: 2024-01-02"
    }
    ```

### Example

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