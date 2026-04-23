import requests

def askLlama(userMessage):
    urls = ["http://localhost:11434/api/chat",
        "https://roboadvisor-gui-mdayryx2vw6ya79omujfoq.streamlit.app/"]

    payload = {
        "model": "mistral",
        "messages": userMessage,
        "stream": False
    }
    for url in urls:
        try:
            response = requests.post(url, json = payload)
            # response.raise_for_status
            # return response.json()['message']['content']
            data = response.json()
            return data["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            return f"Error talking to Llama3 {e}"

