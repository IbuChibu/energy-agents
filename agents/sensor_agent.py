from utils import call_groq_llama_api, summarize_biogas_bursts

def analyze_telemetry(data_24h, weekly_stats, system_name, metadata, user_query, system_type):
    if system_type == "biogas":
        burst_summary = summarize_biogas_bursts(data_24h)

        avg_flow = weekly_stats.get("avg_flow", "N/A")
        max_pressure = weekly_stats.get("max_pressure", "N/A")
        avg_temp = weekly_stats.get("avg_temperature", "N/A")
        total_gas = weekly_stats.get("total_gas_consumption_delta", "N/A")

        meta_desc = (
            f"Location: {metadata.get('location', 'Unknown')}\n"
            f"System Type: Biogas Digester\n"
            f"Capacity: {metadata.get('digester_capacity_m3', 'N/A')} m³\n"
            f"Use Case: {metadata.get('use_case', 'N/A')}"
        )

        prompt = f"""
You are an expert AI analyzing biogas stove sensor data. This system has event-based usage — flow is typically zero and spikes when the stove is used.

System: {system_name}
{meta_desc}

### Weekly Context:
- Average flow: {avg_flow:.2f} L/min
- Max pressure: {max_pressure:.1f} Pa
- Avg temperature: {avg_temp:.2f} °C
- Total gas used: {total_gas:.2f} L

### Past 24h Burst Summary:
- Number of usage bursts: {burst_summary['n_bursts']}
- Maximum flow: {burst_summary['max_flow']} L/min
- Average burst duration (rows): {burst_summary['avg_burst_duration']:.1f}
- Total gas used in last 24h: {burst_summary['total_volume']:.2f} L

Recent bursts (up to 5 rows):
{burst_summary['recent_bursts']}

Task:
1. Analyze the recent gas usage behavior.
2. Identify trends, anomalies, or concerns — e.g., long inactivity, excessive pressure, or burst inefficiency.
3. Highlight anything that may require maintenance or community engagement.
4. Also consider the user’s question: "{user_query}"
"""
        return call_groq_llama_api(prompt)

    elif system_type == "solar":
        avg_bat_temp = weekly_stats.get("avg_bat_temp", "N/A")
        avg_soc = weekly_stats.get("avg_state_of_charge", "N/A")
        avg_load_w = weekly_stats.get("avg_load_w", "N/A")
        avg_solar_w = weekly_stats.get("avg_solar_w", "N/A")

        meta_desc = (
            f"Location: {metadata.get('location', 'N/A')}\n"
            f"System Type: Solar PV (off-grid)\n"
            f"Panel Type: {metadata.get('panel_type', 'N/A')}\n"
        )

        recent_snippet = data_24h.tail(20).to_dict(orient="records")

        prompt = f"""
You are an expert AI analyzing solar panel system telemetry.

System: {system_name}
{meta_desc}

Context from the last 7 days:
- Average battery temperature: {avg_bat_temp:.2f} °C
- Average state of charge: {avg_soc:.2f} %
- Average load power: {avg_load_w:.2f} W
- Average solar power generation: {avg_solar_w:.2f} W

Here are recent telemetry records from the last 24 hours (sample):
{recent_snippet}

User query: {user_query}

Please analyze the recent data in context of the past week. Summarize key performance indicators, trends, any anomalies in battery temperature, state of charge, load power, and solar power generation. Highlight any operational issues or maintenance recommendations.
"""
        return call_groq_llama_api(prompt)

    else:
        return f"(Unsupported system type: {system_type})"