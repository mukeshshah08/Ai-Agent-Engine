from typing import Callable, Dict, Any


TOOLS: Dict[str, Callable[..., Any]] = {}




def register_tool(name: str, fn: Callable[..., Any]):
    TOOLS[name] = fn




def get_tool(name: str):
    return TOOLS.get(name)