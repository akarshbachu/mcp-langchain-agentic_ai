from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import os

from dotenv import load_dotenv
load_dotenv()

import asyncio

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

async def main():
    client = MultiServerMCPClient({
        "weather": {
            "url": "http://127.0.0.1:8000/mcp",# as it is hosted in port 8000 from weather.py
            "transport": "streamable-http"
        }, 
        "math": {
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio"
        }
    })
    tools = await client.get_tools()
    model = ChatGroq(model="llama-3.1-8b-instant")
    agent = create_react_agent(model, tools)
    math_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is (3+2)*10=?"
                }
            ]
        }
    )
    print("Math Agent:", math_response['messages'][-1].content)
    
    weather_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in Hyderabad?"
                }
            ]
        }
    )
    print("Weather Agent:", weather_response['messages'][-1].content)
    
if __name__ == "__main__":
    asyncio.run(main())