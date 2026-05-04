import os

import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "deepseek-llm:7b")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

def generate_response(message:str):
    endpoint = f"{OLLAMA_URL}"
    data={
        "model": MODEL,
        "prompt": message,
        "stream": False
    }
    
    try:
        response=requests.post(endpoint, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        if hasattr(e, "response") and e.response is not None:
            raise RuntimeError(
                f"Error al comunicarse con Ollama: {e.response.status_code} {e.response.text}"
            )
        raise RuntimeError(f"Error al comunicarse con Ollama: {e}")
    
    body= response.json()
    output = body.get("response")
    if not output:
        raise RuntimeError("Ollama devolvió una respuesta vacía")
    return output        