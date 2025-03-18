from transformers import pipeline


# generate SysML v2 textual class specification for a hardware component with Llama 3.3
def generate_component_attributes(component):
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.3-70B-Instruct")
    return pipe([
        { "role": "system", "content": "You generate SysML v2 textual diagram class specifications for hardware with the hardware components that the user gives you. Respond with only the SysML v2 Textual Representation of the singular class, not formatted in any way." },
        { "role": "user", "content": component }
    ])[0]['generated_text']

# generate SysML v2 block definition for a hardware component with Llama 3.3
def generate_sysml(json_data, class_specs):
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.3-70B-Instruct")
    return pipe([
        {"role": "system", "content": f""""
You generate SysML v2 textual diagrams for JSON data of hardware components that the user gives you. The currently-existing component class specifications that you should implement for the hardware are as follows:

```
{class_specs}
```

Respond with only the SysML v2 Textual Representation, not formatted with backticks or with any other formatting.
        """.strip() },
        { "role": "user", "content": json_data }
    ])[0]['generated_text']
