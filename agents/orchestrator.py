from agents.sensor_agent import analyze_telemetry
from agents.alert_agent import detect_alerts
from agents.recommendation_agent import generate_recommendations


def run_all_agents(data_snippet, system_name, system_type):
    summary = analyze_telemetry(data_snippet, system_name, system_type)
    alerts = detect_alerts(data_snippet, system_name, system_type)
    recs = generate_recommendations(data_snippet, system_name, system_type)

    return f"""
### Agent Report for {system_name} ({system_type})

**Summary:**
{summary}

**Alerts:**
{alerts}

**Recommendations:**
{recs}
"""
