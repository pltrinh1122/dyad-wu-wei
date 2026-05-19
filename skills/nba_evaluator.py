"""
NBA Evaluator (Legacy Proxy)
===========================
This skill acts as a thin wrapper around the NBAManager orchestrator 
to maintain backward compatibility for legacy callers.
"""

from orchestrator.mgr_nba import NBAManager

def evaluate(repository: str = "pltrinh1122/agent-antigravity", frontier_file: str = "artifacts/frontier_state.md") -> dict:
    """Evaluates the Next-Best-Action by proxying to NBAManager."""
    nba = NBAManager(repository=repository)
    result = nba.evaluate(frontier_file=frontier_file)
    
    # Map NBAManager result to legacy format for compatibility
    mode = result.get("type", "path_switching")
    recommendations = result.get("recommendations", [])
    
    if mode == "path_continuation":
        message = f"Continuing Path {result.get('path_id')}: {result.get('path_title')}"
    else:
        message = "Path exhausted or not detected. Recommending next best from global backlog."
        
    return {
        "mode": mode,
        "recommended": recommendations,
        "message": message,
        "active_path": result.get("path_id")
    }
