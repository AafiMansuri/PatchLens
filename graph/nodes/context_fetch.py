"""Function of context_fetch node"""


from graph.state import AgentState
from tools.github_client import fetch_file_content


def context_fetch(state: AgentState) -> dict:
    """
    CONTEXT FETCH node - fetches file contents for each file in the plan.

    Iterates over state['plan'], retrieves each file's content via
    GitHub API, and builds a codebase snapshot for the review step.

    Args:
        state: Current agent state containing plan, owner, and repo.

    Returns:
        Dict with fetched_files - a mapping of file paths to their content.
    """

    owner = state["owner"]
    repo = state["repo"]
    plan = state["plan"]
    fetched_files = {}

    for file in plan:
        path = file["file_path"]
        content = fetch_file_content(owner, repo, path)
        if content is not None:
            fetched_files[path] = content
    
    return {"fetched_files": fetched_files}