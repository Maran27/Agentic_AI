from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.agents import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "Math": {
                "command": "python",
                "args": ["MCP/mathserver.py"],
                "transport": "stdio",
            },
            "Weather": {
                "url": "http://localhost:8000/mcp", #we put /mcp to find all the mcp services in the server
                "transport": "streamable-http",
            }
        }
    )

    import os
    os.environ["OPENAI_API_KEY"] = "sk-..."  # Replace with your actual OpenAI API key
    tools = await client.get_tools()
    model = ChatGroq(model="groq:llama3-8b-8192", temperature=0)
    agent = create_react_agent(model, tools)
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is the sum of 5 and 3?"}]}
    )
    print("Math Response:", math_response["messages"][-1].content)
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is the current weather in New York?"}]}
    )
    print("Weather Response:", weather_response["messages"][-1].content)

asyncio.run(main())