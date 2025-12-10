from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional


class NodeDef(BaseModel):
    name: str
    tool: Optional[str] = None


class GraphDef(BaseModel):
    graph_id: str
    nodes: List[NodeDef]
    edges: Dict[str, Any] = Field(default_factory=dict)


class RunResult(BaseModel):
    run_id: str
    graph_id: str
    state: Dict[str, Any]
    log: List[str]
    finished: bool = False
