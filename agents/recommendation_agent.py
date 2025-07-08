from utils import call_groq_llama_api

def generate_recommendations(data_24h, weekly_stats, system_name, metadata, user_query, system_type):
    if system_type == "biogas":
        avg_flow = weekly_stats.get("avg_flow", "N/A")
        max_pressure = weekly_stats.get("max_pressure", "N/A")
        avg_temp = weekly_stats.get("avg_temperature", "N/A")
        total_consumption = weekly_stats.get("total_gas_consumption_delta", "N/A")
        
        meta_desc = (
            f"Location: {metadata.get('location', 'N/A')}\n"
            f"System Type: Biogas Digester\n"
            f"Capacity (m3): {metadata.get('digester_capacity_m3', 'N/A')}\n"
            f"Use Case: {metadata.get('use_case', 'N/A')}\n"
        )
        
        recent_snippet = data_24h.tail(60).to_dict(orient="records")
        
        prompt = f"""
You are an energy system advisor AI focused on biogas stove sensor data.

System: {system_name}
{meta_desc}

Summary stats from past week:
- Average flow: {avg_flow:.2f} L/min
- Max pressure: {max_pressure:.1f} Pa
- Avg temperature: {avg_temp:.2f} °C
- Total gas consumption delta: {total_consumption:.2f} L

Recent telemetry records from last 24 hours:
{recent_snippet}

User query: {user_query}

Provide 2-3 practical recommendations to improve system performance, efficiency, or maintenance scheduling based on the data.
"""
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
You are an energy system advisor AI focused on solar panel telemetry.

System: {system_name}
{meta_desc}

Summary stats from past week:
- Average battery temperature: {avg_bat_temp:.2f} °C
- Average state of charge: {avg_soc:.2f} %
- Average load power: {avg_load_w:.2f} W
- Average solar power generation: {avg_solar_w:.2f} W

Recent telemetry records from last 24 hours:
{recent_snippet}

User query: {user_query}

Provide 2-3 practical recommendations to improve solar system performance, efficiency, or maintenance scheduling based on the data.
"""
    else:
        prompt = f"System type '{system_type}' is not supported."

    return call_groq_llama_api(prompt)