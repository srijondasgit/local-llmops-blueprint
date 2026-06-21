import os
from redis import Redis
from langchain_core.globals import set_llm_cache
from langchain_community.cache import RedisCache
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langfuse.langchain import CallbackHandler
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# 1. Active High-Speed Prompt Caching
# If a user submits an identical prompt, Redis instantly serves it without hitting llama.cpp
set_llm_cache(RedisCache(redis_obj=Redis(host="localhost", port=6379)))

# 2. Bind Langfuse Tracing Callbacks
# Replace these keys with the tokens generated in your local http://localhost:3000 dashboard
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-your-key-here"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-your-key-here"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"
langfuse_handler = CallbackHandler()

# 3. Bind to Local llama.cpp Engine
llm = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed-locally",
    model="mistral-7b"
)

# 4. Construct a Minimal State Graph (LangGraph)
class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

workflow = StateGraph(State)
workflow.add_node("mistral_agent", agent_node)
workflow.add_edge(START, "mistral_agent")
workflow.add_edge("mistral_agent", END)
local_agent = workflow.compile()

# 5. Execute the Workflow
if __name__ == "__main__":
    payload = {"messages": [HumanMessage(content="Explain quantum physics in 4 words.")]}
    config = {"callbacks": [langfuse_handler]}
    
    print("\n--- Sending request to local stack ---")
    for event in local_agent.stream(payload, config=config):
        print(event)
