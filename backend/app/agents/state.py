from typing import TypedDict, Optional, Any


class AgentState(TypedDict, total=False):
    user_query: str
    tool_name: Optional[str]
    tool_args: Optional[dict[str, Any]]
    tool_output: Optional[Any]
    final_response: Optional[str]