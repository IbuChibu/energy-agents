from utils import call_groq_llama_api

def analyze_telemetry(data_snippet, system_name, system_type):
    if system_type == "solar":
        prompt = f"""You are a sensor analysis agent for a solar energy system.

Here is recent telemetry data from {system_name}:
{data_snippet}

Summarize key stats, anomalies, and operating conditions."""
    elif system_type == "biogas":
        prompt = f"""You are a sensor analysis agent for a biogas energy system.

Here is recent telemetry data from {system_name}:
{data_snippet}

Summarize gas flow, pressure trends, and any concerns."""
    else:
        prompt = f"System type '{system_type}' not supported."

    return call_groq_llama_api(prompt)