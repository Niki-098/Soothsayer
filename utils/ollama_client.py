import requests
import json

def query_ollama(prompt, model="tinyllama:latest", ollama_url="http://localhost:11434/api/generate"):
    """
    Optimized for TinyLlama - faster and more reliable
    """
    try:
        # Optimize settings for TinyLlama
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 300,  # Shorter responses for faster processing
                "top_k": 40,
                "top_p": 0.9,
                "repeat_penalty": 1.1
            }
        }
        
        print(f"Querying {model} at {ollama_url}")
        
        response = requests.post(ollama_url, json=payload, timeout=120)  # 2 minute timeout
        response.raise_for_status()
        
        result = response.json()
        
        if "response" in result:
            response_text = result["response"].strip()
            if response_text:
                return response_text
            else:
                return "Model returned empty response. Try rephrasing your question."
        else:
            return f"Unexpected response format: {result}"
            
    except requests.exceptions.Timeout:
        return "⏰ Request timed out. TinyLlama should be faster - try restarting Ollama with 'ollama serve'"
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to Ollama. Make sure 'ollama serve' is running on port 11434"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"❌ Model '{model}' not found. Make sure you ran: ollama pull {model}"
        return f"❌ HTTP Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"