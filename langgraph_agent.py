"""
LangGraph Agent implementation with Microsoft Learn MCP integration
"""
import os
from langchain_openai import AzureChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent


# Global MCP client instance
_mcp_client = None


async def get_mcp_client():
    """Get or create the MCP client instance"""
    global _mcp_client
    
    if _mcp_client is None:
        _mcp_client = MultiServerMCPClient(
            {
                "microsoft_learn": {
                    "transport": "streamable_http",
                    "url": "https://learn.microsoft.com/api/mcp",
                }
            }
        )
    
    return _mcp_client


def create_llm():
    """Create and return Azure OpenAI LLM instance"""
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        temperature=0.7,
    )


async def run_langgraph_agent(query: str) -> str:
    """
    Run the LangGraph agent with MCP tools from Microsoft Learn
    
    Args:
        query: The user's question
        
    Returns:
        The agent's response
    """
    try:
        # Get MCP client
        client = await get_mcp_client()
        
        # Get tools from MCP server
        tools = await client.get_tools()
        
        # Create the LLM
        llm = create_llm()
        
        # Create agent with MCP tools using correct API
        agent = create_agent(
            llm,
            tools,
            system_prompt="""You are a helpful assistant that answers questions about Microsoft documentation.
You have access to the Microsoft Learn documentation through MCP tools.
When answering questions, search for relevant documentation and provide accurate, helpful responses.
Always cite the documentation sources you use and provide detailed explanations with examples when appropriate.
Structure your responses with clear headings and formatting."""
        )
        
        # Run the agent
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        
        # Extract the final response
        if result and "messages" in result:
            # Get the last message which should be the assistant's response
            last_message = result["messages"][-1]
            if hasattr(last_message, 'content'):
                return last_message.content
            return str(last_message)
        
        return str(result)
            
    except Exception as e:
        return f"Error running LangGraph agent with MCP: {str(e)}\n\nPlease check that:\n1. The Microsoft Learn MCP server is accessible\n2. Your Azure OpenAI credentials are correct\n3. Network connectivity is available"
