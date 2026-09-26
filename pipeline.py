from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str):
    state={"topic": topic, "research": "", "report": "", "critique": ""}
    
    #search agent working
    print("\n"+"="*50)
    print("step 1 - search agent is working...")
    print("="*50)
    search_agent=build_search_agent()
    search_agent_response=search_agent.invoke({
        "message":[("user", f"Please use the tools to find information on the topic: {topic}")]
    })
    state["search_results"]=search_agent_response['message'][-1].content
    print("\nSearch Agent Response:\n", state["search_results"])