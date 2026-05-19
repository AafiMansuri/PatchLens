"""Entry Point for the graph"""

from graph.nodes.context_fetch import context_fetch
from graph.nodes.planner import planner
from graph.state import AgentState
from graph.nodes.intake import intake
from langgraph.graph import END, StateGraph

graph = StateGraph(AgentState)
graph.add_node("intake",intake)
graph.add_node("planner",planner)
graph.add_node("context_fetch",context_fetch)

graph.set_entry_point("intake")
graph.add_edge("intake","planner")
graph.add_edge("planner","context_fetch")
graph.add_edge("context_fetch",END)

agent = graph.compile()

state = agent.invoke({"pr_url":"https://github.com/AafiMansuri/DummyRepo/pull/1"})

print("State:\n",state)