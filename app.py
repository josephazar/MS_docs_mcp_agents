import asyncio
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure import AzureOpenAIChatClient
import markdown2
from langgraph_agent import run_langgraph_agent

app = FastAPI(title="Microsoft Docs MCP Agent PoC")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global agent instance (will be initialized on startup)
agent = None
mcp_server = None


@app.on_event("startup")
async def startup_event():
    """Initialize the agent and MCP server on startup"""
    global agent, mcp_server
    
    # Initialize MCP Server for Microsoft Learn Docs
    mcp_server = MCPStreamableHTTPTool(
        name="Microsoft Learn MCP",
        url="https://learn.microsoft.com/api/mcp",
    )
    
    # Initialize Azure OpenAI Chat Client
    chat_client = AzureOpenAIChatClient(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )
    
    # Create the agent with MCP tools
    agent = ChatAgent(
        chat_client=chat_client,
        name="DocsAgent",
        instructions="""You are a helpful assistant that answers questions about Microsoft documentation.
        You have access to the Microsoft Learn documentation through MCP tools.
        When answering questions, search for relevant documentation and provide accurate, helpful responses.
        Always cite the documentation sources you use.""",
    )
    
    print("✅ Agent and MCP server initialized successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global agent, mcp_server
    print("🔴 Shutting down agent and MCP server...")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "query": "", "response": "", "agent_type": "maf"}
    )


@app.post("/query", response_class=HTMLResponse)
async def query(request: Request, query_text: str = Form(...)):
    """Handle query requests to the agent"""
    global agent, mcp_server
    
    if not query_text or not query_text.strip():
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query_text,
                "response": "Please enter a valid query.",
                "error": True,
                "agent_type": "maf"
            }
        )
    
    try:
        # Run the agent with the query and MCP tools
        result = await agent.run(query_text, tools=mcp_server)
        
        response_text = result.text if hasattr(result, 'text') else str(result)
        
        # Convert markdown to HTML
        response_html = markdown2.markdown(
            response_text,
            extras=[
                "fenced-code-blocks",
                "tables",
                "break-on-newline",
                "code-friendly",
                "cuddled-lists",
                "header-ids"
            ]
        )
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query_text,
                "response": response_html,
                "error": False,
                "agent_type": "maf"
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query_text,
                "response": f"Error: {str(e)}",
                "error": True,
                "agent_type": "maf"
            }
        )


@app.post("/query-langgraph", response_class=HTMLResponse)
async def query_langgraph(request: Request, query_text: str = Form(...)):
    """Handle query requests to the LangGraph agent"""
    
    if not query_text or not query_text.strip():
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query_text,
                "response": "Please enter a valid query.",
                "error": True,
                "agent_type": "langgraph"
            }
        )
    
    try:
        # Run the LangGraph agent
        response_text = await run_langgraph_agent(query_text)
        
        # Convert markdown to HTML
        response_html = markdown2.markdown(
            response_text,
            extras=[
                "fenced-code-blocks",
                "tables",
                "break-on-newline",
                "code-friendly",
                "cuddled-lists",
                "header-ids"
            ]
        )
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query_text,
                "response": response_html,
                "error": False,
                "agent_type": "langgraph"
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query_text,
                "response": f"Error: {str(e)}",
                "error": True,
                "agent_type": "langgraph"
            }
        )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_initialized": agent is not None,
        "mcp_server_initialized": mcp_server is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
