from utils import call_groq_llama_api
import pandas as pd

def detect_alerts(data_24h, weekly_stats, system_name, metadata, user_query, system_type):
    if system_type == "biogas":
        avg_flow = weekly_stats.get("avg_flow", "N/A")
        max_pressure = weekly_stats.get("max_pressure", "N/A")
        avg_temp = weekly_stats.get("avg_temperature", "N/A")

        meta = f"{metadata.get('location', 'N/A')}, {metadata.get('use_case', 'N/A')}, {metadata.get('digester_capacity_m3', 'N/A')}m3"

        preview_df = data_24h[["timestamp", "flow", "single_pressure", "temperature"]].tail(10)
        recent_preview = preview_df.to_string(index=False)

        prompt = f"""
You are a monitoring AI for biogas sensors.

System: {system_name} | Metadata: {meta}

Weekly Avg:
- Flow: {avg_flow:.2f}
- Pressure: {max_pressure:.1f}
- Temp: {avg_temp:.2f}

Last 24h Sample (last 10 rows):
{recent_preview}

Task: Identify alerts or unusual patterns. Highlight possible causes and recommend urgent actions. Also consider user query: "{user_query}"
"""
        return call_groq_llama_api(prompt)

    elif system_type == "solar":
        avg_bat_temp = weekly_stats.get("avg_bat_temp", "N/A")
        avg_soc = weekly_stats.get("avg_state_of_charge", "N/A")
        avg_load_w = weekly_stats.get("avg_load_w", "N/A")
        avg_solar_w = weekly_stats.get("avg_solar_w", "N/A")

        meta = f"{metadata.get('location', 'N/A')}, {metadata.get('panel_type', 'N/A')}"

        preview_df = data_24h[["timestamp", "state_of_charge", "solar_w", "load_w"]].tail(10)
        recent_preview = preview_df.to_string(index=False)

        prompt = f"""
You are a monitoring AI for solar panel systems.

System: {system_name} | Metadata: {meta}

Weekly Avg:
- Battery Temp: {avg_bat_temp:.2f}
- State of Charge: {avg_soc:.2f}
- Load Power: {avg_load_w:.2f}
- Solar Power: {avg_solar_w:.2f}

Last 24h Sample (last 10 rows):
{recent_preview}

Task: Detect critical issues or anomalies. Explain severity and suggest quick or preventive fixes. Also respond to user query: "{user_query}"
"""
        return call_groq_llama_api(prompt)

    return f"(Unsupported system type: {system_type})"