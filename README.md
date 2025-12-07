# Microsoft Docs MCP Agent - Dual Framework PoC

A FastAPI application demonstrating two AI agent frameworks (Microsoft Agent Framework and LangGraph) working side-by-side with **full MCP integration** to access Microsoft Learn documentation via Azure OpenAI.

## Overview

This project showcases a comparison platform for AI agent frameworks, allowing users to toggle between Microsoft Agent Framework (MAF) and LangGraph to see how different frameworks handle the same queries against Microsoft documentation.

**Both agents have complete MCP (Model Context Protocol) integration** with the Microsoft Learn MCP Server, providing real-time access to official Microsoft documentation.

## Features

### Dual Agent Framework Support with MCP

#### Microsoft Agent Framework (MAF)
- ✅ **Full MCP Integration** via `MCPStreamableHTTPTool`
- ✅ **Real-time Documentation Access** from Microsoft Learn
- ✅ **Comprehensive Responses** with citations and examples
- ✅ **Native MCP Support** built into the framework

#### LangGraph
- ✅ **Full MCP Integration** via `langchain-mcp-adapters`
- ✅ **Real-time Documentation Access** from Microsoft Learn
- ✅ **Structured Responses** with detailed explanations
- ✅ **Tool-based Architecture** with automatic MCP tool conversion

### Interactive UI
- **Toggle Between Agents** - Switch frameworks with a single click
- **Visual Badges** - Clear indication of which agent generated each response (MAF/LangGraph)
- **Markdown Rendering** - Beautiful formatting with headings, code blocks, lists, and links
- **Responsive Design** - Professional Microsoft-themed interface

### Technical Features
- Server-side rendering with Jinja2
- Real-time markdown to HTML conversion
- MCP server integration for both frameworks
- Error handling with visual feedback
- Health check endpoint
- Clean, maintainable code structure

## Architecture

```
User Browser
    ↓
FastAPI (Port 8000)
    ↓
    ├─→ Microsoft Agent Framework → Azure OpenAI → MCP Server → Microsoft Learn Docs
    └─→ LangGraph → Azure OpenAI → MCP Server → Microsoft Learn Docs
```

## Prerequisites

- Python 3.11+
- Azure OpenAI resource with deployed model (gpt-4o-mini recommended)
- Internet connection for MCP server access

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/josephazar/MS_docs_mcp_agents.git
cd MS_docs_mcp_agents
```

### 2. Create virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your Azure OpenAI credentials:

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

## Running the Application

### Start the server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the application
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Access the application

Open your browser and navigate to:
- **Application:** http://localhost:8000
- **Health Check:** http://localhost:8000/health

## Usage

1. **Select Agent Framework** - Click either "Microsoft Agent Framework" or "LangGraph" button
2. **Enter Your Question** - Type a question about Microsoft technologies
3. **Submit** - Click "Ask Agent" to get a response
4. **View Results** - See the formatted response with the agent badge

### Example Queries

- "What is Azure Functions and how do I create one?"
- "How do I deploy a web app to Azure App Service using Azure CLI?"
- "What is Azure Kubernetes Service?"
- "Explain Azure Container Instances"
- "How do I create an Azure SQL Database?"

## API Endpoints

### `GET /`
Home page with agent toggle and query form

### `POST /query`
Submit query to Microsoft Agent Framework
- **Form Parameter:** `query_text` (string)
- **Returns:** HTML response with MAF answer from MCP

### `POST /query-langgraph`
Submit query to LangGraph agent
- **Form Parameter:** `query_text` (string)
- **Returns:** HTML response with LangGraph answer from MCP

### `GET /health`
Health check endpoint
- **Returns:** JSON with agent initialization status

## Project Structure

```
MS_docs_mcp_agents/
├── app.py                           # Main FastAPI application
├── langgraph_agent.py               # LangGraph agent with MCP integration
├── templates/
│   └── index.html                  # Jinja2 template with toggle UI
├── static/                         # Static files directory
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── MCP_INTEGRATION_SUCCESS.md      # MCP integration test results
```

## Technologies Used

### Backend
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Microsoft Agent Framework** - AI agent orchestration with native MCP support
- **LangGraph** - Graph-based agent framework
- **LangChain** - LLM application framework
- **langchain-mcp-adapters** - MCP integration for LangChain/LangGraph
- **Markdown2** - Markdown to HTML conversion

### AI/ML
- **Azure OpenAI** - Language model provider (gpt-4o-mini)
- **Microsoft Learn MCP Server** - Real-time documentation access

### Frontend
- **Jinja2** - Template engine
- **HTML5/CSS3** - Modern web standards
- **JavaScript** - Interactive toggle functionality

## MCP Integration Details

### Microsoft Agent Framework
```python
from agent_framework import MCPStreamableHTTPTool

mcp_server = MCPStreamableHTTPTool(
    name="Microsoft Learn MCP",
    url="https://learn.microsoft.com/api/mcp",
)

agent = ChatAgent(
    chat_client=chat_client,
    name="DocsAgent",
    instructions="..."
)

result = await agent.run(query, tools=mcp_server)
```

### LangGraph
```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient({
    "microsoft_learn": {
        "transport": "streamable_http",
        "url": "https://learn.microsoft.com/api/mcp",
    }
})

tools = await client.get_tools()
agent = create_agent(llm, tools, system_prompt="...")
result = await agent.ainvoke({"messages": [...]})
```

## Comparison: MAF vs LangGraph (Both with Full MCP)

| Feature | Microsoft Agent Framework | LangGraph |
|---------|---------------------------|-----------|
| **MCP Integration** | ✅ Native via MCPStreamableHTTPTool | ✅ Via langchain-mcp-adapters |
| **Documentation Access** | ✅ Real-time via MCP | ✅ Real-time via MCP |
| **Setup Complexity** | Medium | Medium |
| **Response Quality** | Excellent with citations | Excellent with details |
| **Tool Conversion** | Automatic | Automatic |
| **Customization** | High | Very High |
| **Framework Maturity** | Stable | Stable |

## Configuration

### Environment Variables

All configuration is done through environment variables in the `.env` file:

- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key
- `AZURE_OPENAI_API_VERSION` - API version (default: 2024-12-01-preview)
- `AZURE_OPENAI_DEPLOYMENT_NAME` - Your deployed model name

### MCP Server

The Microsoft Learn MCP Server is publicly accessible at:
- **Endpoint:** https://learn.microsoft.com/api/mcp
- **Transport:** Streamable HTTP
- **Authentication:** None required
- **Documentation:** Full Microsoft Learn documentation

## Troubleshooting

### Agent not responding
- Verify Azure OpenAI credentials in `.env`
- Check that deployment name matches your Azure resource
- Ensure internet connectivity for MCP server

### MCP connection errors
- Verify MCP server is accessible: https://learn.microsoft.com/api/mcp
- Check firewall settings
- Ensure `streamable_http` transport is configured correctly

### Import errors
- Confirm virtual environment is activated
- Reinstall packages: `pip install -r requirements.txt`
- Check Python version (3.11+ required)

### Port already in use
- Change port in `app.py` or use: `uvicorn app:app --port 8001`

### Environment variables not loading
- Ensure `.env` file exists in project root
- Check file permissions
- Manually export variables if needed

## Performance

- **Startup Time:** ~2-3 seconds
- **MAF Query Response Time:** ~10-15 seconds (includes MCP calls and LLM processing)
- **LangGraph Query Response Time:** ~8-12 seconds (includes MCP calls and LLM processing)
- **MCP Server Response:** Fast and reliable
- **UI Rendering:** Instant
- **Toggle Response:** Immediate

## Development

### Adding new features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with both agents
5. Submit a pull request

### Code style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and small
- Test with both agent frameworks

## Testing

### Manual Testing
1. Start the application
2. Toggle between MAF and LangGraph
3. Submit test queries
4. Verify MCP integration is working
5. Check markdown rendering
6. Confirm responses are from Microsoft Learn docs

### Example Test Queries
- Azure Functions
- Azure App Service
- Azure Kubernetes Service
- Azure Container Instances
- Azure SQL Database

## License

This project is provided as-is for demonstration and educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Microsoft Agent Framework team
- LangGraph and LangChain communities
- Azure OpenAI team
- Microsoft Learn documentation team
- Anthropic for the Model Context Protocol (MCP) specification

## Related Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [LangChain MCP Adapters](https://docs.langchain.com/oss/python/langchain/mcp)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
