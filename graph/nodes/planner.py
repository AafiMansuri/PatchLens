"""Function of planner node"""

import json
from graph.state import AgentState
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


system_prompt = """
You are a PR review planning agent.

Your job is NOT to review the code.

Your job is to determine the minimal additional code context required
to perform a high-quality pull request review.

You are given:
- changed files
- git diffs/patches
- file metadata
- list of all file paths in the repository

Analyze the diffs and identify which additional files should be fetched.

Focus on:
- imported modules
- parent classes/interfaces
- related tests
- schemas/types/contracts
- configs/constants/env definitions
- utility functions referenced in changed code
- neighboring files necessary for understanding logic flow

Avoid unnecessary context expansion.

Only request files that are likely necessary for understanding:
- correctness
- side effects
- API compatibility
- architectural impact
- security implications
- test coverage

For each requested file:
- provide exact file path when possible
- explain why the file is needed

Guidelines:
- Prefer precision over breadth
- Do not recursively speculate deeply
- Avoid fetching entire directories
- Avoid unrelated imports
- If diff is self-contained, return empty list
- Tests are important when business logic changes
- Config/schema files are important when contracts change
- Shared utilities are important when modified behavior depends on them
- Request no more than 10 files.
- Return an empty list [] if no additional context is needed.

Output ONLY valid JSON.

Schema:

[
  {
    "file_path": string,
    "reasoning": string
  }
]
"""

def planner(state: AgentState) -> dict:
  """
  PLANNING node - LLM analyzes diffs and determines which additional
  files need to be fetched for a thorough review.

  Args:
      state: Current agent state containing pr_metadata, changed_files, and repo_files.

  Returns:
      Dict with plan - a list of dicts containing file_path and reasoning.
  """
  pr_metadata = state['pr_metadata']

  repo_files = "\n".join(state['repo_files'])

  diffs = ""

  for file in state['changed_files']:
    diffs += f"### {file['filename']} ({file['status']})\n{file['patch']}\n\n"

  user_message = f"""
  ## PR title
  {pr_metadata['title']}

  ## PR Description
  {pr_metadata['desc']}

  ## Changed Files and Diffs
  {diffs}

  ## Repository Files
  {repo_files}
  """

  llm = ChatGroq(model='llama-3.3-70b-versatile', temperature=0)

  messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=user_message)
  ]

  response = llm.invoke(messages)

  content = response.content.strip()
  content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

  try:
    plan = json.loads(content)
  except:
    print("Failed to parse LLM response")
    plan = []
  
  return {"plan":plan}
