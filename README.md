# AI Agent Engine

This repository contains a minimal FastAPI project that implements a simple workflow (graph) execution engine and an example agent workflow.

---

## How to Run

### 1. Create and activate a virtual environment
python -m venv .venv
..venv\Scripts\Activate.ps1

### 2. Install dependencies
pip install -r requirements.txt

### 3. Start the FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

### 4. Open API documentation
http://127.0.0.1:8000/docs

### 5. Run the example workflow
Create a `payload.json`:
```json
{
  "graph_id": "code_review_v1",
  "state": {
    "code": "def f1():\n    pass\n\n# TODO fix\n\ndef f2():\n    pass"
  },
  "max_iterations": 100
}

curl -X POST http://127.0.0.1:8000/graph/run -H "Content-Type: application/json" -d @payload.json
```
## What the Workflow Engine Supports

- Executes nodes in a directed graph (workflow)
- Nodes pass and update shared state
- Supports branching and looping via `_next`
- Tracks logs for each step of execution
- Stops loops using:
  - max iterations
  - threshold improvements
  - stagnation detection
- Stores run results in memory and can be retrieved using `run_id`

---

## What I Would Improve With More Time

- Add a real database instead of in-memory storage
- Add async node execution and parallelism
- Add a visual workflow editor
- Improve error handling and validation
- Add real LLM-based node behavior instead of simple heuristics
- Add configuration for dynamic graphs and workflows
