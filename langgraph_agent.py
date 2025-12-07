"""
LangGraph Agent implementation with Microsoft Learn MCP integration
"""
import os
from typing import TypedDict, Annotated, Sequence
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent


# Define the state for our agent
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]


# Initialize Azure OpenAI
def create_llm():
    """Create and return Azure OpenAI LLM instance"""
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        temperature=0.7,
    )


# Main function to run the agent
async def run_langgraph_agent(query: str) -> str:
    """
    Run the LangGraph agent with the given query
    
    Args:
        query: The user's question
        
    Returns:
        The agent's response
    """
    try:
        # Create the LLM
        llm = create_llm()
        
        # For now, use direct LLM call without MCP tools
        # This is a simplified version that works with Azure OpenAI
        system_message = SystemMessage(content="""You are a helpful assistant that answers questions about Microsoft documentation.
You provide accurate, helpful responses about Microsoft Azure, .NET, and other Microsoft technologies.
When answering questions, provide detailed explanations with examples when appropriate.
Always structure your responses with clear headings and formatting.""")
        
        human_message = HumanMessage(content=query)
        
        # Invoke the LLM directly
        response = await llm.ainvoke([system_message, human_message])
        
        return response.content
            
    except Exception as e:
        return f"Error running LangGraph agent: {str(e)}\n\nNote: This is using a simplified LangGraph implementation with direct Azure OpenAI calls. For full MCP integration, additional configuration is required."
