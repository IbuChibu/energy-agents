import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()  # Load .env variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("Groq API key loaded:", GROQ_API_KEY is not None)

# Load telemetry data safely
try:
    solar_data = pd.read_csv("data/solar_telemetry.csv")
except FileNotFoundError:
    solar_data = pd.DataFrame()
    st.warning("Solar telemetry data file not found.")

try:
    biogas_data = pd.read_csv("data/biogas_telemetry.csv")
except FileNotFoundError:
    biogas_data = pd.DataFrame()
    st.warning("Biogas telemetry data file not found.")

# Map system names to IDs and data
system_options = {
    "Solar Site A": {"id": "S1", "data": solar_data},
    "Biogas Site B": {"id": "B1", "data": biogas_data},
}

def call_groq_llama_api(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
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
    st.write("Select an energy system and ask questions about its telemetry.")

    selected_system = st.selectbox("Choose an energy system:", list(system_options.keys()))

    user_query = st.text_area(
        "Enter a question or command for the AI agent:",
        f"Please analyze and report on the latest data from {selected_system}."
    )

    if st.button("Run Agent"):
        system_info = system_options[selected_system]
        df = system_info["data"]

        if df.empty:
            st.error(f"No telemetry data available for {selected_system}.")
            return

        # Prepare latest telemetry snippet (last 5 rows)
        latest_rows = df.tail(5).to_dict(orient="records")

        system_prompt = (
            f"You are an AI assistant monitoring {selected_system} (System ID: {system_info['id']}).\n\n"
            f"Here are the latest telemetry records (last 5 rows):\n{latest_rows}\n\n"
            f"Please answer the user's question based on this data."
        )

        full_prompt = f"{system_prompt}\n\nUser question: {user_query}"

        response = call_groq_llama_api(full_prompt)

        st.subheader("AI Agent Response")
        st.write(response)

if __name__ == "__main__":
    main()