import glob
import pandas as pd

# read all csv files in data folder into pandas dataframe
def read_data():
    df = pd.DataFrame()

    for filename in glob.glob('data/*.csv'):
        df = pd.concat([df, pd.read_csv(filename)])

    return df

# print json representation of data
df = read_data()
print(df.to_json(orient='records'))
