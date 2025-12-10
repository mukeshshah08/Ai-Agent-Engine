from datetime import datetime

def log_line(node: str, message: str) -> str:
    ts = datetime.utcnow().isoformat() + "Z"
    return f"[{ts}] [{node}] {message}"
