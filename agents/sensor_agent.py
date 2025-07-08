from utils import call_groq_llama_api, summarize_biogas_bursts
import pandas as pd

def analyze_telemetry(data_24h, weekly_stats, system_name, metadata, user_query, system_type):
    if system_type == "biogas":
        burst_summary = summarize_biogas_bursts(data_24h)

        avg_flow = weekly_stats.get("avg_flow", "N/A")
        max_pressure = weekly_stats.get("max_pressure", "N/A")
        avg_temp = weekly_stats.get("avg_temperature", "N/A")
        total_gas = weekly_stats.get("total_gas_consumption_delta", "N/A")

        meta = f"{metadata.get('location', 'Unknown')}, {metadata.get('use_case', 'N/A')}, {metadata.get('digester_capacity_m3', 'N/A')}m3"

        # Format recent burst rows (max 5 rows only)
        recent_bursts = burst_summary.get("recent_bursts", pd.DataFrame())
        if isinstance(recent_bursts, pd.DataFrame):
            burst_preview = recent_bursts[["start_time", "duration", "volume"]].head(5).to_string(index=False)
        else:
            burst_preview = str(recent_bursts)[:500]

        prompt = f"""
You are an expert AI analyzing biogas sensor data (event-based usage).

System: {system_name} | Metadata: {meta}

Weekly Stats:
- Avg Flow: {avg_flow:.2f}
- Max Pressure: {max_pressure:.1f}
- Avg Temp: {avg_temp:.2f}
- Weekly Gas Used: {total_gas:.2f}

Last 24h Burst Summary:
- Bursts: {burst_summary['n_bursts']}
- Max Flow: {burst_summary['max_flow']}
- Avg Burst Duration: {burst_summary['avg_burst_duration']:.1f}
- 24h Gas Used: {burst_summary['total_volume']:.2f}

Recent Bursts (up to 5):
{burst_preview}

Question: {user_query}
Briefly analyze recent usage, highlight any issues or anomalies, and respond to the query.
"""
        return call_groq_llama_api(prompt)

    elif system_type == "solar":
        avg_bat_temp = weekly_stats.get("avg_bat_temp", "N/A")
        avg_soc = weekly_stats.get("avg_state_of_charge", "N/A")
        avg_load_w = weekly_stats.get("avg_load_w", "N/A")
        avg_solar_w = weekly_stats.get("avg_solar_w", "N/A")

        meta = f"{metadata.get('location', 'N/A')}, Panel: {metadata.get('panel_type', 'N/A')}"

        # Create compact preview of last 10 rows
        preview_df = data_24h[["timestamp", "state_of_charge", "solar_w", "load_w"]].tail(10)
        recent_preview = preview_df.to_string(index=False)

        prompt = f"""
You are an expert AI analyzing solar telemetry.

System: {system_name} | Metadata: {meta}

7-day Averages:
- Battery Temp: {avg_bat_temp:.2f}
- SoC: {avg_soc:.2f}
- Load: {avg_load_w:.2f}
- Solar Gen: {avg_solar_w:.2f}

Recent 24h Snapshot (latest 10 records):
{recent_preview}

Question: {user_query}
Summarize performance, flag anomalies, and answer the query concisely.
"""
        return call_groq_llama_api(prompt)

    else:
        return f"(Unsupported system type: {system_type})"