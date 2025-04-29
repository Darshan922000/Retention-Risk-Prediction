from typing import Any, Dict
from typing_extensions import TypedDict


# Graph state
class State(TypedDict):
    input_data: Dict[str, Any]  # user query
    response: str  # response
