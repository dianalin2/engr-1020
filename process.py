import glob
import pandas as pd
# from llm import generate_component_attributes, generate_sysml

# read all csv files in data folder into pandas dataframe
def read_data(filename):
    df = pd.DataFrame()

    # for filename in glob.glob('data/*.csv'):
    df = pd.concat([df, pd.read_csv(filename)])

    return df

# print json representation of data

# generate sysml v2 textual class specification for a hardware component based on the column names of the dataframe
# uml_class = generate_component_attributes(df.columns.tolist())

# # for each row in the dataframe, generate sysml v2 block definition
# for row in df.iterrows():
#     row = row[1].to_dict()

#     # generate sysml v2 block definition for a hardware component
#     uml_block = generate_sysml(row, uml_class)
#     print(uml_block)
    