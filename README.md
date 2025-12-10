# 🚀 AI Agent Engine — Workflow Graph Execution System  
*A minimal workflow engine built using FastAPI, created as part of an AI Engineering Internship assignment.*

---

## 📌 Overview

This project implements a **Mini Workflow Engine** capable of:

- Executing nodes in a directed graph  
- Passing and updating shared state between nodes  
- Supporting branching & looping via `_next` transitions  
- Logging execution steps  
- Storing run results in-memory  
- Providing a full FastAPI backend  

The included example workflow (`code_review_v1`) performs:

1. Extract functions  
2. Estimate complexity  
3. Detect issues  
4. Suggest improvements (looped refinement)

---

## 🗂️ Project Structure
```
app/
├── main.py
├── graph/
│ ├── engine.py
│ ├── models.py
├── workflows/
│ └── code_review.py
├── utils/
│ └── logs.py
├── db/
│ └── memory.py
payload.json
requirements.txt
README.md
```

---

# ▶️ How to Run the Server

### 1. Move into project folder
```powershell
cd "D:\AI Agent Engine"
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```
###Start server
```
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
