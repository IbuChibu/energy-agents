import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()  # Load .env variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("Groq API key loaded:", GROQ_API_KEY is not None)
solar_data = pd.read_csv("data/solar_telemetry.csv")
biogas_data = pd.read_csv("data/biogas_telemetry.csv")

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
    st.write("Select a system and deploy an AI agent.")

    # System options
    systems = ["Solar Site A", "Biogas Site B"]
    selected_system = st.selectbox("Choose an energy system:", systems)

    # Optional: custom user query
    user_query = st.text_area("Enter a question or command for the AI agent:", 
                              f"Monitor and report on {selected_system}.")

    if st.button("Run Agent"):
        response = call_groq_llama_api(user_query)
        st.subheader("AI Agent Response")
        st.write(response)

if __name__ == "__main__":
    main()