from utils import call_groq_llama_api

def generate_recommendations(data_snippet, system_name, system_type):
    prompt = f"""You are an energy advisor AI for a {system_type} system.

Here is recent data from {system_name}:
{data_snippet}

Provide 2–3 practical recommendations to improve performance or efficiency."""
    return call_groq_llama_api(prompt)
