# llama_api.py

import requests
import json
from config import OLLAMA_API_URL, MODEL_NAME, HEADERS

def query_llama_api(prompt):
    """
    Sends a prompt to the Ollama API and retrieves the response.
    Args:
        prompt (str): User query to send to the API.
    Returns:
        str: Response text or an error message.
    """
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for HTTP issues
        response_data = response.json()
        return response_data.get("response", "")
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Error: {http_err.response.status_code} - {http_err.response.reason}"
    except requests.exceptions.RequestException as req_err:
        return f"Request Error: {req_err}"
    except json.JSONDecodeError as json_err:
        return f"JSON Decode Error: {json_err}"