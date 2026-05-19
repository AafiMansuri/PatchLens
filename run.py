"""Entry Point for the graph"""

from graph.nodes.planner import planner
from graph.state import AgentState
from graph.nodes.intake import intake
from langgraph.graph import StateGraph

graph = StateGraph(AgentState)
graph.add_node("intake",intake)
graph.add_node("planner",planner)

graph.set_entry_point("intake")
graph.set_finish_point("intake")
graph.add_edge("intake","planner")

agent = graph.compile()

state = agent.invoke({"pr_url":"https://github.com/AafiMansuri/DummyRepo/pull/1"})

print("State:\n",state)