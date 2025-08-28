import requests

def askLlama(userMessage):
    url = "http://localhost:11434/api/chat"

    payload = {
        "model": "mistral",
        "messages": userMessage,
        "stream": False
    }

    try:
        response = requests.post(url, json = payload)
        # response.raise_for_status
        # return response.json()['message']['content']
        data = response.json()
        return data["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        return f"Error talking to Llama3 {e}"

