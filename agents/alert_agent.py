from utils import call_groq_llama_api

def detect_alerts(data_24h, weekly_stats, system_name, metadata):
    # Extract relevant stats
    avg_flow = weekly_stats.get("avg_flow", "N/A")
    max_pressure = weekly_stats.get("max_pressure", "N/A")
    avg_temp = weekly_stats.get("avg_temperature", "N/A")
    
    meta_desc = (
        f"Location: {metadata.get('location', 'N/A')}\n"
        f"System Type: Biogas Digester\n"
        f"Capacity (m3): {metadata.get('digester_capacity_m3', 'N/A')}\n"
        f"Use Case: {metadata.get('use_case', 'N/A')}\n"
    )
    
    recent_snippet = data_24h.tail(60).to_dict(orient="records")
    
    prompt = f"""
You are a critical alert monitoring AI for a biogas stove sensor system.

System: {system_name}
{meta_desc}

Context from last 7 days:
- Average flow rate: {avg_flow:.2f} L/min
- Maximum gas pressure recorded: {max_pressure:.1f} Pa
- Average gas temperature: {avg_temp:.2f} °C

Here are the recent telemetry records from the last 24 hours (sample):
{recent_snippet}

Identify any critical alerts, unusual patterns, or abnormalities. Describe the severity and potential causes. Suggest urgent actions if necessary.
"""
    return call_groq_llama_api(prompt)