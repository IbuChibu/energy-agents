import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("Groq API key loaded:", GROQ_API_KEY is not None)

def call_groq_llama_api(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",  # You can use "llama3-70b-8192" if needed
        "messages": [
            {"role": "system", "content": "You are an energy monitoring assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"API call failed: {response.status_code} - {response.text}"

def main():
    st.title("Energy Agents AI Dashboard")

    st.write("Welcome! Press the button to talk to AI.")

    if st.button("Talk to AI"):
        prompt = "Hello AI, show me the status of energy systems."
        response = call_groq_llama_api(prompt)
        st.write("AI says:", response)

if __name__ == "__main__":
    main()