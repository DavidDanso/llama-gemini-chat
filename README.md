# LangChain Multi-Model API

A FastAPI-powered backend with Streamlit frontend that orchestrates multiple LLM providers (Google Gemini & Ollama) for creative content generation. Built with LangChain for seamless model switching and LangServe for production-ready REST endpoints.

## Architecture

**Backend:** FastAPI server exposing LangChain chains as REST endpoints via LangServe  
**Frontend:** Streamlit client with tabbed UI for essay and poem generation  
**Models:**

- **Gemini 2.5 Flash** (via Google GenAI API) → Essay generation
- **Llama 3.2** (via Ollama local runtime) → Poem generation

## Project Structure

```
llama-gemini-chat/
├── api/
│   ├── app.py      # FastAPI server with LangServe routes
│   └── client.py   # Streamlit UI client
├── requirements.txt
├── .env            # API keys (not committed)
└── .gitignore
```

## App Preview:

<table width="100%"> 
<tr>
<td width="50%">      
&nbsp; 
<br>
<p align="center">
  Main Feed
</p>
<img src="https://github.com/DavidDanso/llama-gemini-chat/blob/main/ui/main-feed.png" />
</td> 
<td width="50%">
<br>
<p align="center">
  LLM Response
</p>
<img src="https://github.com/DavidDanso/llama-gemini-chat/blob/main/ui/response.png" />
</td>
</table>

## Core Components

### `api/app.py` - FastAPI Server

Initializes three LangServe routes:

- `/gemini` - Direct Gemini model access (generic chat)
- `/essay` - Prompt-templated essay generation via Gemini
- `/poem` - Prompt-templated poem generation via Ollama Llama

**Key Implementation Details:**

- Uses `ChatPromptTemplate` for structured prompt engineering
- Chains prompts with models using LangChain's `|` operator
- Loads `GOOGLE_API_KEY` from environment with validation
- API Runs on `127.0.0.1:8000` by default

### `api/client.py` - Streamlit Client

Dual-tab interface for hitting LangServe endpoints:

- Tab 1: Essay Generator → `POST /essay/invoke`
- Tab 2: Poem Generator → `POST /poem/invoke`

**Request Format:**

```python
{
  "input": {
    "topic": "your_topic_here"
  }
}
```

**Response Handling:**

- Parses `output.content` for dict responses
- Falls back to raw `output` for string responses
- 120s timeout for long-running LLM calls

## Prerequisites

1. **Ollama Runtime** (for local Llama inference)

   ```bash
   # Install Ollama: https://ollama.ai
   ollama pull llama3.2 or anyother model
   ```

2. **Google API Key** (for Gemini access)
   - Get key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Setup

1. **Clone & Install Dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**

   ```bash
   # Create .env file
   GOOGLE_API_KEY=your_actual_google_api_key
   LANGCHAIN_API_KEY=your_langchain_key  # Optional for tracing
   LANGCHAIN_PROJECT_NAME=ChatBotProject
   ```

3. **Verify Ollama**
   ```bash
   ollama list  # Should show llama3.2
   ```

## Usage

### 1. Start FastAPI Server

```bash
python api/app.py
# Server runs on http://127.0.0.1:8000
# Docs at http://127.0.0.1:8000/docs
```

### 2. Launch Streamlit UI

```bash
streamlit run api/client.py
# Opens browser at http://localhost:8501
```

### 3. API Usage (cURL)

```bash
# Generate essay
curl -X POST http://localhost:8000/essay/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": {"topic": "quantum computing"}}'

# Generate poem
curl -X POST http://localhost:8000/poem/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": {"topic": "outer space"}}'
```

## Key Dependencies

| Package                  | Purpose                               |
| ------------------------ | ------------------------------------- |
| `fastapi` + `uvicorn`    | ASGI server framework                 |
| `langchain_google_genai` | Gemini model integration              |
| `langchain_ollama`       | Ollama local model wrapper            |
| `langserve`              | Exposes LangChain chains as REST APIs |
| `streamlit`              | Frontend UI builder                   |
| `python-dotenv`          | Environment variable management       |

## Development Notes

- **Prompt Templates:** Hardcoded to 100-word outputs for consistency
- **Model Selection:** Essays use Gemini (cloud), poems use Llama (local) to demonstrate hybrid deployment
- **Error Handling:** Client includes 120s timeout + structured exception handling
- **LangServe Routes:** Auto-generates OpenAPI schemas at `/docs` for all chains

## Troubleshooting

**Ollama Connection Errors:**

```bash
# Ensure Ollama service is running
ollama serve  # If not running as daemon
```

**Gemini API Errors:**

- Verify `GOOGLE_API_KEY` in `.env` is valid
- Check quota at Google Cloud Console

**Port Conflicts:**

```bash
# Change FastAPI port in app.py
uvicorn.run(app, host="127.0.0.1", port=8001)
```
