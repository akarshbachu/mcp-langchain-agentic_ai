# MCP LangChain - Agentic AI

This repository demonstrates the integration of the **Model Context Protocol (MCP)** with **LangChain** and **LangGraph** to build a multi-tool agentic AI system.
Course: https://www.youtube.com/watch?v=rV3HJ4LEZ7k&t=28393s

---

## 📖 Introduction to Model Context Protocol (MCP)

**Model Context Protocol (MCP)** is an open standard designed to connect Large Language Models (LLMs) to data sources, local systems, and external APIs securely and efficiently. Rather than writing custom integration code for every API or tool, MCP provides a unified API interface.

### Foundational Blocks of MCP
1. **Client**: The orchestrator or LLM-powered application (e.g., LangChain/LangGraph) that queries servers to discover and invoke tools.
2. **Server**: Lightweight programs that expose specific capabilities (**Tools**, **Resources**, or **Prompts**) to the client.
3. **Transport Layers**: The protocol channel through which clients and servers communicate:
   - **`stdio`**: Standard Input/Output. The client launches the server as a local subprocess and communicates using stdin/stdout. Ideal for local execution.
   - **`streamable-http` (SSE)**: HTTP-based Server-Sent Events. The server runs as a web service (e.g., via FastAPI/uvicorn). Ideal for remote or distributed microservices.

---

## 🗺️ Architectural Flow

Here is how the components in this repository interact:

```
+-------------------------------------------------------------+
|                     CLIENT APPLICATION                      |
|                                                             |
|    +-----------------------+                                |
|    |    LangGraph Agent    |                                |
|    +-----------+-----------+                                |
|                |                                            |
|                | (Uses Tools)                               |
|                v                                            |
|    +-----------+-----------+          (API Calls)           |
|    | MultiServerMCPClient  +------------------------------> | [ Groq API ]
|    +-----+-----------+-----+                                | (Llama 3.1 Model)
+----------|-----------|--------------------------------------+
           |           |
    (stdio)|           | (streamable-http over Network)
           v           v
   +-------+----+   +--+---------------+
   | MathServer |   |  WeatherServer   |
   | (Local Sub |   | (Port 8000 /mcp) |
   |  Process)  |   |                  |
   +------------+   +------------------+
```

---

## 🛠️ Project Technicalities

This project implements two MCP servers and a unified LangChain client:

### 1. Math Server (`mathserver.py`)
* **Transport**: Local `stdio` (Stdio-based communication).
* **Capabilities**: Exposes basic arithmetic tools (`add`, `multiply`, `sub`, `divide`).
* **Execution**: Started automatically by the client as a background subprocess.

### 2. Weather Server (`weather.py`)
* **Transport**: Network-native `streamable-http` (exposes endpoints on `/mcp`).
* **Capabilities**: Exposes a `get_weather` tool.
* **Execution**: Runs independently on port `8000`.

### 3. Unified Client (`client.py`)
* Uses `MultiServerMCPClient` to orchestrate both the Math and Weather servers.
* Automatically fetches all tools from both servers during runtime.
* Binds the tools to a **LangGraph React Agent** powered by Groq's `llama-3.1-8b-instant` model.

---

## 🚀 Step-by-Step Setup & Execution

### 1. Environment Setup
We use the **`uv`** package manager for fast, reliable dependency management.

```powershell
# Install UV (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Initialize virtual environment
uv venv

# Activate the virtual environment
.venv\Scripts\activate

# Install all dependencies
uv add -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start the Weather MCP Server
Since the Weather Server runs over HTTP (`streamable-http`), it must be started manually so the client can connect to it:
```powershell
uv run python weather.py
```
*The server will start running on `http://127.0.0.1:8000/mcp`.*

> [!NOTE]
> **What about the Math Server?**
> You do **not** need to run `mathserver.py` in a separate terminal. Because it is configured with the `stdio` transport, the client (`client.py`) will automatically spawn it as a background subprocess when it starts.

### 4. Run the Agent Client
In a new terminal (with the virtual environment activated), run the client application:
```powershell
uv run python client.py
```

### Expected Output
The client will connect to both servers, fetch their tools, invoke the LLM agent, and output responses:
```
Math Agent: The answer to (3+2)*10 is 50.
Weather Agent: The current weather in Hyderabad is 25 degrees Celsius and sunny.
```