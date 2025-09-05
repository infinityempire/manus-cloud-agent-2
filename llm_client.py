
import os, requests

API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.1-8b-instant")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def chat(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": MODEL,
        "messages": [{"role": "system", "content": "Answer concisely."}, {"role": "user", "content": prompt}],
    }
    r = requests.post(API_URL, json=body, headers=headers)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
