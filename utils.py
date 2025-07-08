import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def call_groq_llama_api(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for energy systems."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"API error: {response.status_code} - {response.text}"

def slice_last_24h(df, timestamp_col="timestamp"):
    if timestamp_col not in df.columns:
        raise ValueError(f"Timestamp column '{timestamp_col}' not found in dataframe.")
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], utc=True)
    last_timestamp = df[timestamp_col].max()
    start_time = last_timestamp - pd.Timedelta(hours=24)
    df_24h = df[df[timestamp_col] > start_time].copy()
    return df_24h

def compute_biogas_weekly_stats(df):
    # Defensive numeric conversion
    for col in ["flow", "single_pressure", "temperature", "gas_consumption_delta"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    stats = {
        "avg_flow": df["flow"].mean() if "flow" in df.columns else None,
        "max_pressure": df["single_pressure"].max() if "single_pressure" in df.columns else None,
        "avg_temperature": df["temperature"].mean() if "temperature" in df.columns else None,
        "total_gas_consumption_delta": df["gas_consumption_delta"].sum() if "gas_consumption_delta" in df.columns else None,
    }
    return stats