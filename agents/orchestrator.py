from agents.sensor_agent import analyze_telemetry
from agents.alert_agent import detect_alerts
from agents.recommendation_agent import generate_recommendations
from utils import compute_biogas_weekly_stats, compute_solar_weekly_stats
import pandas as pd

def run_all_agents(full_data: pd.DataFrame, system_name: str, system_type: str, metadata: dict, user_query: str) -> str:
    full_data["timestamp"] = pd.to_datetime(full_data["timestamp"], utc=True)
    last_24h = full_data[full_data["timestamp"] >= (full_data["timestamp"].max() - pd.Timedelta(hours=24))]

    if system_type == "biogas":
        weekly_stats = compute_biogas_weekly_stats(full_data)
    elif system_type == "solar":
        weekly_stats = compute_solar_weekly_stats(full_data)
    else:
        weekly_stats = {}

    summary = analyze_telemetry(last_24h, weekly_stats, system_name, metadata, user_query, system_type)
    alerts = detect_alerts(last_24h, weekly_stats, system_name, metadata, user_query, system_type)
    recommendations = generate_recommendations(last_24h, weekly_stats, system_name, metadata, user_query, system_type)

    return f"""
### Agent Report for {system_name} ({system_type})

**Summary:**
{summary}

**Alerts:**
{alerts}

**Recommendations:**
{recommendations}
"""



