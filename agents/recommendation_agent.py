from utils import call_groq_llama_api

def generate_recommendations(data_24h, weekly_stats, system_name, metadata, user_query, system_type):
    if system_type == "biogas":
        avg_flow = weekly_stats.get("avg_flow", "N/A")
        max_pressure = weekly_stats.get("max_pressure", "N/A")
        avg_temp = weekly_stats.get("avg_temperature", "N/A")
        total_consumption = weekly_stats.get("total_gas_consumption_delta", "N/A")

        meta = f"{metadata.get('location', 'N/A')}, {metadata.get('use_case', 'N/A')}, Capacity: {metadata.get('digester_capacity_m3', 'N/A')}m3"

        preview_df = data_24h[["timestamp", "flow", "single_pressure", "temperature"]].tail(10)
        recent_preview = preview_df.to_string(index=False)

        prompt = f"""
You are an energy system advisor AI for biogas stove sensors.

System: {system_name} | Metadata: {meta}

Weekly Summary:
- Avg flow: {avg_flow:.2f} L/min
- Max pressure: {max_pressure:.1f} Pa
- Avg temperature: {avg_temp:.2f} °C
- Total gas consumed: {total_consumption:.2f} L

Recent telemetry sample (last 10 rows):
{recent_preview}

Task: Provide 2-3 practical recommendations to improve performance, efficiency, or maintenance based on data and user query: "{user_query}"
"""
        return call_groq_llama_api(prompt)

    elif system_type == "solar":
        avg_bat_temp = weekly_stats.get("avg_bat_temp", "N/A")
        avg_soc = weekly_stats.get("avg_state_of_charge", "N/A")
        avg_load_w = weekly_stats.get("avg_load_w", "N/A")
        avg_solar_w = weekly_stats.get("avg_solar_w", "N/A")

        meta = f"{metadata.get('location', 'N/A')}, Panel: {metadata.get('panel_type', 'N/A')}"

        preview_df = data_24h[["timestamp", "state_of_charge", "solar_w", "load_w"]].tail(10)
        recent_preview = preview_df.to_string(index=False)

        prompt = f"""
You are an energy system advisor AI for solar panel telemetry.

System: {system_name} | Metadata: {meta}

Weekly Summary:
- Avg battery temp: {avg_bat_temp:.2f} °C
- Avg state of charge: {avg_soc:.2f} %
- Avg load power: {avg_load_w:.2f} W
- Avg solar power: {avg_solar_w:.2f} W

Recent telemetry sample (last 10 rows):
{recent_preview}

Task: Provide 2-3 practical recommendations to improve performance, efficiency, or maintenance based on data and user query: "{user_query}"
"""
        return call_groq_llama_api(prompt)

    return f"(Unsupported system type: {system_type})"