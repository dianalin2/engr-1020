from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from dotenv import load_dotenv
import os
from process import read_data
import sys

load_dotenv()

# get the list of models to generate from the path specified in the command line arguments
df = read_data(sys.argv[1])

uri = os.getenv("DB_uri")

# create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["engr1020"]

data = db["data"]

# have some identifier that is unique so that data will only appear once in the database
db.data.create_index([("Asset Identifier", pymongo.ASCENDING), ("Serial Number"), ("Location ID")], unique=True)
data.insert_many(df.to_dict(orient = 'records'), ordered = False)
