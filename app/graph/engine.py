from typing import Dict, Any, List, Optional
import uuid
from .models import GraphDef, RunResult
from ..db.memory import GRAPHS, RUNS
from ..utils.logs import log_line
from ..graph.registry import get_tool


class GraphEngine:
    def create_graph(self, graph: GraphDef):
        if graph.graph_id in GRAPHS:
            raise ValueError("Graph already exists")
        # store plain dict
        GRAPHS[graph.graph_id] = {
            "nodes": [n.dict() for n in graph.nodes],
            "edges": graph.edges,
        }
        return graph.graph_id

    def _resolve_next(self, current: str, state: Dict[str, Any], edges: Dict[str, Any]) -> Optional[str]:
        # Priority: state['_next'] if provided by node
        if state.get("_next"):
            nxt = state.pop("_next")
            return nxt
        # else static edge
        edge = edges.get(current)
        if not edge:
            return None
        # if edge is string
        if isinstance(edge, str):
            return edge
        # if edge is dict with conditions - support 'default' key
        if isinstance(edge, dict):
            return edge.get("default")
        # list fallback
        if isinstance(edge, list) and edge:
            return edge[0]
        return None

    def run_graph(self, graph_id: str, initial_state: Dict[str, Any], max_iterations: int = 1000) -> RunResult:
        graph = GRAPHS.get(graph_id)
        if not graph:
            raise ValueError("Graph not found")
        nodes = {n["name"]: n for n in graph["nodes"]}
        edges = graph["edges"]

        run_id = str(uuid.uuid4())
        state = dict(initial_state)
        log: List[str] = []

        current_node = graph["nodes"][0]["name"] if graph["nodes"] else None
        if current_node is None:
            raise ValueError("Graph has no nodes")

        iterations = 0
        while current_node:
            if iterations >= max_iterations:
                log.append(log_line("engine", "Max iterations reached; aborting loop"))
                break
            iterations += 1

            log.append(log_line(current_node, f"Starting node. State snapshot keys: {list(state.keys())}"))

            node_def = nodes.get(current_node)
            tool_name = node_def.get("tool") if node_def else None
            try:
                if tool_name:
                    tool = get_tool(tool_name)
                    if not tool:
                        log.append(log_line(current_node, f"Tool '{tool_name}' not found"))
                    else:
                        res = tool(state)
                        if isinstance(res, dict):
                            state.update(res)
                            log.append(log_line(current_node, f"Tool '{tool_name}' executed; merged keys: {list(res.keys())}"))
                else:
                    # Support nodes implemented as callable in state under '_node_funcs'
                    funcs = state.get("_node_funcs", {})
                    fn = funcs.get(current_node)
                    if fn:
                        res = fn(state)
                        if isinstance(res, dict):
                            state.update(res)
                            log.append(log_line(current_node, f"Node function executed; merged keys: {list(res.keys())}"))
                    else:
                        log.append(log_line(current_node, "No tool or node function; skipping"))

            except Exception as e:
                log.append(log_line(current_node, f"Exception: {e}"))
                break

            # Decide next node
            next_node = self._resolve_next(current_node, state, edges)
            log.append(log_line(current_node, f"Next -> {next_node}"))
            current_node = next_node

        cleaned_state = {k: v for k, v in state.items() if not k.startswith("_")}

        result = RunResult(run_id=run_id, graph_id=graph_id, state=cleaned_state, log=log, finished=True)
        RUNS[run_id] = result.dict()
        return result

    def get_run(self, run_id: str) -> Optional[RunResult]:
        r = RUNS.get(run_id)
        if not r:
            return None
        return RunResult(**r)

    def list_graphs(self):
        return list(GRAPHS.keys())
