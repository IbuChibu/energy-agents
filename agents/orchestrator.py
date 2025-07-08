from agents.sensor_agent import analyze_telemetry
from agents.alert_agent import detect_alerts
from agents.recommendation_agent import generate_recommendations
import pandas as pd

def calculate_biogas_weekly_stats(df: pd.DataFrame) -> dict:
    # Defensive: convert columns to numeric if not already
    df["flow"] = pd.to_numeric(df["flow"], errors="coerce")
    df["single_pressure"] = pd.to_numeric(df["single_pressure"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["gas_consumption_delta"] = pd.to_numeric(df["gas_consumption_delta"], errors="coerce")

    stats = {
        "avg_flow": df["flow"].mean(),
        "max_pressure": df["single_pressure"].max(),
        "avg_temperature": df["temperature"].mean(),
        "total_gas_consumption_delta": df["gas_consumption_delta"].sum(),
    }
    return stats

def run_all_agents(full_data: pd.DataFrame, system_name: str, system_type: str, metadata: dict) -> str:
    # Slice last 24 hours - assumes timestamp is sorted ascending
    # Timestamp expected as ISO string, convert to datetime
    full_data["timestamp"] = pd.to_datetime(full_data["timestamp"], utc=True)
    last_24h = full_data[full_data["timestamp"] >= (full_data["timestamp"].max() - pd.Timedelta(hours=24))]

    # Calculate weekly stats (currently only biogas, add solar logic later)
    weekly_stats = {}
    if system_type == "biogas":
        weekly_stats = calculate_biogas_weekly_stats(full_data)

    summary = analyze_telemetry(last_24h, system_name, system_type)
    alerts = detect_alerts(last_24h, weekly_stats, system_name, metadata)
    recommendations = generate_recommendations(last_24h, weekly_stats, system_name, metadata)

    return f"""
### Agent Report for {system_name} ({system_type})

**Summary:**
{summary}

**Alerts:**
{alerts}

**Recommendations:**
{recommendations}
"""

