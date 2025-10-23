from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langserve import add_routes
from dotenv import load_dotenv
import uvicorn
import os

# ---------------------------------------------------------------------
# Environment Configuration
# ---------------------------------------------------------------------
load_dotenv()  # Load environment variables from .env file

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in environment variables.")

# Set the environment variable for Google API
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ---------------------------------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------------------------------
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server demonstrating LangChain integration with Gemini and Ollama models.",
)

# ---------------------------------------------------------------------
# Model Initialization
# ---------------------------------------------------------------------

# Google Gemini 2.5 Flash model
gemini_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Ollama Llama 3.2 model
ollama_model = OllamaLLM(model="llama3.2")

# ---------------------------------------------------------------------
# Prompt Templates
# ---------------------------------------------------------------------
essay_prompt = ChatPromptTemplate.from_template(
    "Write a 100-word essay about {topic}."
)

poem_prompt = ChatPromptTemplate.from_template(
    "Write a 100-word poem about {topic} suitable for a 5-year-old child."
)

# ---------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------

# Route for Gemini model (generic chat)
add_routes(app, gemini_model, path="/gemini")

# Route for essay generation using Gemini
add_routes(app, essay_prompt | gemini_model, path="/essay")

# Route for poem generation using Llama
add_routes(app, poem_prompt | ollama_model, path="/poem")

# ---------------------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
