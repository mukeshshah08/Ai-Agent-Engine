from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph.models import NodeDef, GraphDef
from app.graph.engine import GraphEngine
from app.workflows import code_review
from app.db import memory

app = FastAPI(title="Mini Workflow Engine")
engine = GraphEngine()


class CreateGraphReq(BaseModel):
    graph_id: str
    nodes: list
    edges: dict


class RunReq(BaseModel):
    graph_id: str
    state: dict
    max_iterations: int = 100


@app.post("/graph/create")
async def create_graph(req: CreateGraphReq):
    nodes = [NodeDef(name=n) if isinstance(n, str) else NodeDef(**n) for n in req.nodes]
    graph = GraphDef(graph_id=req.graph_id, nodes=nodes, edges=req.edges)
    try:
        engine.create_graph(graph)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"graph_id": req.graph_id}


@app.post("/graph/run")
async def run_graph(req: RunReq):
    if req.graph_id not in memory.GRAPHS:
        raise HTTPException(status_code=404, detail="Graph not found")
    state = dict(req.state)
    # attach Python node functions for this example
    state["_node_funcs"] = code_review.node_funcs()
    try:
        res = engine.run_graph(req.graph_id, state, max_iterations=req.max_iterations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"final_state": res.state, "log": res.log, "run_id": res.run_id}


@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    r = engine.get_run(run_id)
    if not r:
        raise HTTPException(status_code=404, detail="Run not found")
    return r.dict()


@app.get("/graphs")
async def list_graphs():
    return {"graphs": engine.list_graphs()}


@app.on_event("startup")
async def startup_event():
    example_graph = {
        "graph_id": "code_review_v1",
        "nodes": [
            "extract_functions",
            "check_complexity",
            "detect_issues",
            "suggest_improvements"
        ],
        "edges": {
            "extract_functions": "check_complexity",
            "check_complexity": "detect_issues",
            "detect_issues": "suggest_improvements",
            "suggest_improvements": None
        }
    }

    nodes = [NodeDef(name=n) for n in example_graph["nodes"]]
    graph = GraphDef(graph_id=example_graph["graph_id"], nodes=nodes, edges=example_graph["edges"])
    try:
        engine.create_graph(graph)
    except Exception:
        # already exists or any other non-fatal error
        pass
