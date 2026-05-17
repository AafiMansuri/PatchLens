from typing import TypedDict


class AgentState(TypedDict):
    """
    Shared state for the PR review agent workflow.
    """
    owner: str
    repo: str
    pr_number: int
    pr_url: str
    pr_metadata: dict           # {title, description, author, branches}
    changed_files: list[dict]   # [{filename, status, contents_url, patch}]
    fetched_files: dict         # {filename: content} - empty initially
    plan: list[str]             # files the planner wants to fetch
    review_comments: list[dict] # {file, line, severity, category, comment, suggested_fix} - empty initially