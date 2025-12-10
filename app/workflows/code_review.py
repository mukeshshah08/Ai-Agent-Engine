from typing import Dict, Any

THRESHOLD = 7

def extract_functions(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    funcs = []
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("def "):
            name = line.split("def ")[1].split("(")[0].strip()
            funcs.append(name)
    return {"functions": funcs}

def check_complexity(state: Dict[str, Any]) -> Dict[str, Any]:
    funcs = state.get("functions", [])
    complexity = len(funcs) * 2 + max(0, len(state.get("code", "")) // 100)
    return {"complexity_score": complexity}

def detect_issues(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    issues = 0
    for line in code.splitlines():
        if "TODO" in line:
            issues += 1
        if len(line) > 120:
            issues += 1
    return {"issues": issues}

def suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    issues = state.get("issues", 0)
    complexity = state.get("complexity_score", 0)

    # track attempts to avoid infinite loops
    loop_key = "_suggest_attempts"
    attempts = state.get(loop_key, 0) + 1
    state[loop_key] = attempts

    # realistic improvement: increase quality score each iteration
    previous_quality = state.get("quality_score", 0)
    quality_score = previous_quality + 2  # improvement per cycle

    # reduce issues gradually
    issues = max(0, issues - 1)

    THRESHOLD = 7
    MAX_ATTEMPTS = 5

    # Stop looping if we reached threshold OR hit max attempts
    if quality_score >= THRESHOLD or attempts >= MAX_ATTEMPTS:
        # cleanup internal tracking key
        state.pop(loop_key, None)

        return {
            "issues": issues,
            "quality_score": quality_score
        }

    # Otherwise continue looping this node
    return {
        "issues": issues,
        "quality_score": quality_score,
        "_next": "suggest_improvements"
    }



def node_funcs():
    return {
        "extract_functions": extract_functions,
        "check_complexity": check_complexity,
        "detect_issues": detect_issues,
        "suggest_improvements": suggest_improvements,
    }
