import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

# Import the orchestrator function that runs all agents
from agents.orchestrator import run_all_agents

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("Groq API key loaded:", GROQ_API_KEY is not None)

# Load telemetry data safely
try:
    solar_data = pd.read_csv("data/solar_telemetry.csv")
except FileNotFoundError:
    solar_data = pd.DataFrame()
    st.warning("Solar telemetry data file not found.")

try:
    biogas_data = pd.read_csv("data/biogas_telemetry.csv")
except FileNotFoundError:
    biogas_data = pd.DataFrame()
    st.warning("Biogas telemetry data file not found.")

# Map system names to IDs and data
system_options = {
    "Solar Site A": {"id": "S1", "data": solar_data},
    "Biogas Site B": {"id": "B1", "data": biogas_data},
}

def main():
    st.title("Energy Agents AI Dashboard")
    st.write("Select an energy system and ask questions about its telemetry.")

    selected_system = st.selectbox("Choose an energy system:", list(system_options.keys()))

    user_query = st.text_area(
        "Enter a question or command for the AI agent:",
        f"Please analyze and report on the latest data from {selected_system}."
    )

    if st.button("Run Agent"):
        system_info = system_options[selected_system]
        df = system_info["data"]

        if df.empty:
            st.error(f"No telemetry data available for {selected_system}.")
            return

        # Dynamically select recent rows based on system type
        if system_info["id"] == "B1":
            recent_rows = df.tail(120).to_dict(orient="records")  # Biogas: last 2 hours (1-min intervals)
            system_type = "biogas"
        else:
            recent_rows = df.tail(8).to_dict(orient="records")    # Solar: last 2 hours (15-min intervals)
            system_type = "solar"

        system_name = selected_system

        # Add user query to prompt if needed inside the orchestrator or here
        # For now, just run the agents on data
        report = run_all_agents(recent_rows, system_name, system_type)

        st.subheader("AI Agent Report")
        st.markdown(report)

if __name__ == "__main__":
    main()