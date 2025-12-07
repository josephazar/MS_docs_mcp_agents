# Microsoft Docs MCP Agent - Dual Framework PoC

A FastAPI application demonstrating two AI agent frameworks (Microsoft Agent Framework and LangGraph) working side-by-side with Microsoft Learn MCP Server integration and Azure OpenAI.

## Overview

This project showcases a comparison platform for AI agent frameworks, allowing users to toggle between Microsoft Agent Framework (MAF) and LangGraph to see how different frameworks handle the same queries against Microsoft documentation.

## Features

### Dual Agent Framework Support
- **Microsoft Agent Framework (MAF)** - Full MCP integration with Microsoft Learn documentation
- **LangGraph** - Direct Azure OpenAI integration with structured responses

### Interactive UI
- **Toggle Between Agents** - Switch frameworks with a single click
- **Visual Badges** - Clear indication of which agent generated each response (MAF/LangGraph)
- **Markdown Rendering** - Beautiful formatting with headings, code blocks, lists, and links
- **Responsive Design** - Professional Microsoft-themed interface

### Technical Features
- Server-side rendering with Jinja2
- Real-time markdown to HTML conversion
- Error handling with visual feedback
- Health check endpoint
- Clean, maintainable code structure

## Architecture

```
User Browser
    ↓
FastAPI (Port 8000)
    ↓
    ├─→ Microsoft Agent Framework → Azure OpenAI → MCP Server
    └─→ LangGraph → Azure OpenAI
```

## Prerequisites

- Python 3.11+
- Azure OpenAI resource with deployed model (gpt-4o-mini recommended)
- Internet connection for MCP server access

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/MS_docs_mcp_agents.git
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

# Load environment variables and run
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
- "Explain Azure Virtual Networks"

## API Endpoints

### `GET /`
Home page with agent toggle and query form

### `POST /query`
Submit query to Microsoft Agent Framework
- **Form Parameter:** `query_text` (string)
- **Returns:** HTML response with MAF answer

### `POST /query-langgraph`
Submit query to LangGraph agent
- **Form Parameter:** `query_text` (string)
- **Returns:** HTML response with LangGraph answer

### `GET /health`
Health check endpoint
- **Returns:** JSON with agent initialization status

## Project Structure

```
MS_docs_mcp_agents/
├── app.py                  # Main FastAPI application
├── langgraph_agent.py      # LangGraph agent implementation
├── templates/
│   └── index.html         # Jinja2 template with toggle UI
├── static/                # Static files directory
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technologies Used

### Backend
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Microsoft Agent Framework** - AI agent orchestration
- **LangGraph** - Graph-based agent framework
- **LangChain** - LLM application framework
- **Markdown2** - Markdown to HTML conversion

### AI/ML
- **Azure OpenAI** - Language model provider (gpt-4o-mini)
- **Microsoft Learn MCP Server** - Documentation access

### Frontend
- **Jinja2** - Template engine
- **HTML5/CSS3** - Modern web standards
- **JavaScript** - Interactive toggle functionality

## Comparison: MAF vs LangGraph

| Feature | Microsoft Agent Framework | LangGraph |
|---------|---------------------------|-----------|
| MCP Integration | ✅ Full native support | ⚠️ Simplified implementation |
| Documentation Access | ✅ Via MCP Server | ❌ Not implemented in this PoC |
| Setup Complexity | Medium | Low |
| Response Quality | Excellent with citations | Excellent, general knowledge |
| Customization | High | Very High |

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
- **Authentication:** None required

## Troubleshooting

### Agent not responding
- Verify Azure OpenAI credentials in `.env`
- Check that deployment name matches your Azure resource
- Ensure internet connectivity for MCP server

### Import errors
- Confirm virtual environment is activated
- Reinstall packages: `pip install -r requirements.txt`

### Port already in use
- Change port in `app.py` or use: `uvicorn app:app --port 8001`

### Environment variables not loading
- Ensure `.env` file exists in project root
- Check file permissions
- Manually export variables if needed

## Development

### Adding new features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and small

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
