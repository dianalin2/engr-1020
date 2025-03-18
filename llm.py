# Use a pipeline as a high-level helper
from transformers import pipeline

prompt = [
    {"role": "system", "content": "You generate SysML v2 textual diagrams for JSON data that the user gives you. Respond with only the SysML v2 Textual Representation, not formatted in any way."}
]

pipe = pipeline("text-generation", model="meta-llama/Llama-3.3-70B-Instruct")

def generate_sysml(json_data):
    return pipe(prompt + [{
        "role": "user",
        "content": json_data
    }])[0]['generated_text']
