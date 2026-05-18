"""Function of the intake node"""

from graph.state import AgentState
from tools.github_client import parse_url, fetch_pr_metadata, fetch_changed_files

def intake(state:AgentState) -> AgentState:
    """
    INTAKE node: fetches PR metadata and changed files from GitHub.

    Parses the PR URL from state, validates the PR is open,
    and retrieves metadata and diffs via the GitHub API.

    Args:
        state: Current agent state containing pr_url.

    Returns:
        Dict with owner, repo, pr_number, pr_metadata, and changed_files.

    Raises:
        ValueError: If the URL is invalid or the PR is not open.
    """

    pr_url = state['pr_url']
    owner, repo, pr_number = parse_url(pr_url)
    pr_metadata = fetch_pr_metadata(owner, repo, pr_number)

    if pr_metadata['state'] != 'open':
        raise ValueError(f"PR is not open, current state: {state}")
    
    changed_files = fetch_changed_files(owner,repo,pr_number)
    
    state['owner'] = owner
    state['repo'] = repo
    state['pr_number'] = pr_number
    state['pr_url'] = pr_url
    state['pr_metadata'] = pr_metadata
    state['changed_files'] = changed_files

    return {
        "owner": owner,
        "repo": repo,
        "pr_number": pr_number,
        "pr_url": pr_url,
        "pr_metadata": pr_metadata,
        "changed_files": changed_files
    }   