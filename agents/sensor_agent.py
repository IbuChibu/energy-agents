from utils import call_groq_llama_api

def analyze_telemetry(data_24h, weekly_stats, system_name, metadata):
    # Unpack stats
    avg_flow = weekly_stats.get("avg_flow", "N/A")
    max_pressure = weekly_stats.get("max_pressure", "N/A")
    avg_temp = weekly_stats.get("avg_temperature", "N/A")
    total_consumption = weekly_stats.get("total_gas_consumption_delta", "N/A")
    
    # Prepare metadata description
    meta_desc = (
        f"Location: {metadata.get('location', 'N/A')}\n"
        f"System Type: Biogas Digester\n"
        f"Capacity (m3): {metadata.get('digester_capacity_m3', 'N/A')}\n"
        f"Use Case: {metadata.get('use_case', 'N/A')}\n"
    )
    
    # Convert recent data snippet to dict (limit to e.g. last 60 rows for prompt brevity)
    recent_snippet = data_24h.tail(60).to_dict(orient="records")
    
    prompt = f"""
You are an expert AI analyzing biogas stove sensor data.

System: {system_name}
{meta_desc}

Context from the last 7 days:
- Average flow: {avg_flow:.2f} L/min
- Maximum pressure recorded: {max_pressure:.1f} Pa
- Average temperature: {avg_temp:.2f} °C
- Total gas consumption delta: {total_consumption:.2f} L

Here are recent telemetry records from the last 24 hours (sample):
{recent_snippet}

Please analyze the recent data in context of the past week. Summarize usage patterns, trends, and any anomalies or concerns in flow, pressure, temperature, and gas consumption. Highlight any operational issues or potential maintenance needs.
"""
    return call_groq_llama_api(prompt)