from tools import web_search_tool
from prompt import autonomous_agent_prompt #hari
from build_agent import build_agent, run_agent
from dotenv import load_dotenv
import os
 
# Load .env file
load_dotenv()
 
########################################
# 1. Define Behavioral Prompt
########################################
 
def web_search_agent(query):
    user_prompt = f"User query: {query}"
    prompt = autonomous_agent_prompt + user_prompt #hari
    tools_list = [web_search_tool] #hari
    agent = build_agent(tools_list)
    response = run_agent(agent, prompt)
    return response
 
 
support_prompt = "Customer is frustrated with delayed shipping and wants a refund"
print(web_search_agent(support_prompt))
