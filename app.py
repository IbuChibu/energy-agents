import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
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

# Load metadata dynamically
try:
    system_metadata_df = pd.read_csv("data/system_metadata.csv")
    system_metadata = system_metadata_df.set_index('system_id').to_dict(orient='index')
except FileNotFoundError:
    system_metadata = {}
    st.warning("System metadata file not found.")

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
        system_id = system_info["id"]
        df = system_info["data"]

        if df.empty:
            st.error(f"No telemetry data available for {selected_system}.")
            return

        # Get metadata for this system
        metadata = system_metadata.get(system_id, {})

        # Pass full df (not just recent rows) for context + user query
        system_type = "biogas" if system_id == "B1" else "solar"

        report = run_all_agents(df, selected_system, system_type, metadata, user_query)

        st.subheader("AI Agent Report")
        st.markdown(report)

if __name__ == "__main__":
    main()