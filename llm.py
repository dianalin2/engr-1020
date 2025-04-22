from transformers import pipeline
import json

def to_camel_case(space_separated_string, lower_first=True):
    words = space_separated_string.split()
    words[0] = words[0].lower() if lower_first else words[0].capitalize()
    return words[0] + ''.join(word.capitalize() for word in words[1:])

# generate SysML v2 textual class specification for a hardware component with Llama 3.2
def generate_component_attributes(component):
    return ''.join([
        "class HardwareAsset {\n",
        ''.join([f"    attribute {to_camel_case(k)}: String;\n" for k in component]),
        "}\n"
    ])

# generate SysML v2 block definition for a hardware component with Llama 3.2
def generate_sysml(json_data, class_specs):
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
    part_name = pipe([
        {"role": "system", "content": '''
You generate descriptions for JSON-formatted inventory details for hardware components that the user gives you.

Respond with only the short description, upper camelcased, not formatted with backticks or with any other formatting. Only respond with alphanumeric characters, no spaces. An example of a generated description is as follows:
        '''.strip() },
        { "role": "user", "content": json_data }
    ], max_new_tokens=128)[0]['generated_text'][-1]['content']

    return ''.join([
        f"part {part_name[0].upper() + part_name[1:].replace(' ', '')}: HardwareAsset {{\n",
        ''.join([f"    attribute {to_camel_case(k)} = \"{v}\";\n" for k, v in json.loads(json_data).items() if k != "_id"]),
        "}\n"
    ])
