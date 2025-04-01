from transformers import pipeline

# generate SysML v2 textual class specification for a hardware component with Llama 3.2
def generate_component_attributes(component):
    # pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-11B-Vision-Instruct")
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
    # pipe = pipeline("text-generation", model="meta-llama/Llama-3.3-70B-Instruct")
    return pipe([
        { "role": "system", "content": """You generate SysML v2 textual diagram class specifications for hardware with the hardware components that the user gives you. Respond with only the SysML v2 Textual Representation of the singular class, not formatted in any way. An example of a generated class (where "class" and "attribute" are keywords) is as follows:
class HardwareAsset {
    attribute assetIdentifier: String;
    attribute manufacturer: String;
    attribute modelNumber: String;
    attribute assetName: String;
    attribute serialNumber: String;
    attribute comments: String;
    attribute assetCostAmount: Real;
    attribute netBookValueAmount: Real;
    attribute ownership: String;
    attribute inventoryDate: Date;
    attribute datePlacedInService: Date;
    attribute usefulLifePeriods: Integer;
    attribute assetType: String;
    attribute oldTagNumber: String;
    attribute locationID: String;
    attribute buildingName: String;
    attribute buildingNumber: String;
    attribute floor: String;
    attribute roomNumber: String;
}
""" },
        { "role": "user", "content": component }
    ], max_new_tokens=512)[0]['generated_text'][-1]['content']

# generate SysML v2 block definition for a hardware component with Llama 3.2
def generate_sysml(json_data, class_specs):
    # pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-11B-Vision-Instruct")
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
    print(json_data)
    # pipe = pipeline("text-generation", model="meta-llama/Llama-3.3-70B-Instruct")
    return pipe([
        {"role": "system", "content": '''
You generate SysML v2 textual diagrams for JSON data of hardware components that the user gives you. The currently-existing component class specifications that you should implement for the hardware are as follows:

```''' + class_specs + '''
```

Respond with only the SysML v2 Textual Representation, not formatted with backticks or with any other formatting.

An example of a generated block definition (where "part" is a keyword) is as follows:

part hardwareAsset1: HardwareAsset {
    assetIdentifier = "77020";
    manufacturer = "TECHNICAL MFG CO.";
    modelNumber = "77A-440-02";
    assetName = "TABLE W/VIBRATION ISOLATIONSYSTEM";
    serialNumber = "2001238";
    comments = "S. RAY TAYLOR";
    assetCostAmount = 5460.37;
    netBookValueAmount = 0.0;
    ownership = "11 UVA Owned";
    inventoryDate = "2022-05-19";
    datePlacedInService = "1997-09-24";
    usefulLifePeriods = 120;
    assetType = "562 Other Lab Equipment";
    oldTagNumber = "77020";
    locationID = "FM_0270_03_362";
    buildingName = "304 Research Lab";
    buildingNumber = "BL0270";
    floor = "03";
    roomNumber = "362";
}
        '''.strip() },
        { "role": "user", "content": json_data }
    ], max_new_tokens=512)[0]['generated_text'][-1]['content']
