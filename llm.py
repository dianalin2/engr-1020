# Use a pipeline as a high-level helper
from transformers import pipeline

prompt = [
    {"role": "system", "content": "You generate SysML v2 textual diagrams for JSON data of hardware components that the user gives you. Respond with only the SysML v2 Textual Representation, not formatted in any way."}
]

def generate_component_attributes(component):
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.3-70B-Instruct")
    return pipe(prompt + [
        { "role": "system", "content": "Please generate the attributes of the following component:" },
        { "role": "user", "content": component }
    ])[0]['generated_text']

def generate_sysml(json_data):
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.3-70B-Instruct")
    return pipe(prompt + [{
        "role": "user",
        "content": json_data
    }])[0]['generated_text']
