from utils import call_groq_llama_api

def detect_alerts(data_snippet, system_name, system_type):
    prompt = f"""You are an alert monitoring agent for {system_type} systems.

Here is recent telemetry data from {system_name}:
{data_snippet}

Identify any critical alerts or abnormalities, and describe severity."""
    return call_groq_llama_api(prompt)