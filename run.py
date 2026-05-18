"""Entry Point for the graph"""

from graph.state import AgentState
from graph.nodes.intake import intake
from langgraph.graph import StateGraph

graph = StateGraph(AgentState)
graph.add_node("intake",intake)
graph.set_entry_point("intake")
graph.set_finish_point("intake")

agent = graph.compile()

state = agent.invoke({"pr_url":"https://github.com/AafiMansuri/DummyRepo/pull/1"})

print(state)