"""
Github Client to interact with the Github API
"""

import base64
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_BASE_URL = "https://api.github.com"
headers = { "Authorization": f"Bearer {GITHUB_TOKEN}" }


def parse_url(url: str):
    """
    Parse and validate a GitHub Pull Request URL

    Expected format:
        https://github.com/<owner>/<repo>/pull/<pr_number>

    Args:
        url: GitHub PR URL

    Returns:
        Tuple(owner, repo, pr_number)
    
    Raises:
        ValueError: If the URL is not a valid GitHub PR URL.
    """

    match = re.match(r"^https://github\.com/([^/]+)/([^/]+)/pull/(\d+)/?$",url)

    if not match:
        raise ValueError("Invalid GitHub PR URL")
    
    owner, repo, pr_number = match.groups()

    return owner, repo, int(pr_number)


def fetch_pr_metadata(owner:str, repo:str, pr_number:int):
    """
    Fetch PR title, author, branches, and description

    Args:
        owner:str
        repo:str
        pr_number:int

    Returns:
        dict(
            title:str,
            author:str,
            branches:dict
            desc:str
            state:str
        )
    """

    url = f"{GITHUB_BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"

    response = requests.get(url=url,headers=headers).json()

    branches = {
        "head": response["head"]["ref"],
        "base": response["base"]["ref"]
    }

    pr_metadata = {
        "title": response["title"],
        "author": response["user"]["login"],
        "branches": branches,
        "desc": response["body"],
        "state": response["state"],
        "head_sha": response["head"]["sha"]
    }

    return pr_metadata


def fetch_changed_files(owner:str, repo:str, pr_number:int):
    """
    Fetch metadata of changed files

    Args:
        owner: name of the repo owner
        repo: name of the repo
        pr_number: pull request number

    Returns:
        list(
            dict(
                filename:str,
                status:str,
                contents_url:str
                patch:str
        ))
    """

    url = f"{GITHUB_BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = requests.get(url=url,headers=headers).json()
    
    changed_files = []
    for file in response:
        changed_file = {
            "filename": file["filename"],
            "status": file["status"],
            "contents_url": file["contents_url"],
            "patch": file.get("patch", "")
        }

        changed_files.append(changed_file)
    
    return changed_files


def fetch_file_tree(owner:str, repo:str, tree_sha: str):
    """
    Fetch file tree of the repo and returns a list containing all file paths.

    Args:
        owner: name of the repo owner
        repo: name of the repo
        tree_sha: the SHA1 value of the tree

    Returns:
        list of file paths
    """

    url = f"{GITHUB_BASE_URL}/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1"

    response = requests.get(url=url, headers=headers).json()

    return [item["path"] for item in response["tree"] if item["type"] == "blob"]


def fetch_file_content(owner:str, repo:str, path: str):
    """
    Fetch content of the file at the provided path in the repository.

    Args:
        owner: name of the repo owner
        repo: name of the repo
        path: path of the file

    Returns:
        content: decoded content of the file
    """

    url = f"{GITHUB_BASE_URL}/repos/{owner}/{repo}/contents/{path}"

    response = requests.get(url=url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    content = base64.b64decode(data["content"]).decode("utf-8")

    return content