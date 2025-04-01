from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from dotenv import load_dotenv
import os
from process import read_data
import sys

load_dotenv()

df = read_data(sys.argv[1])

uri = os.getenv("DB_uri")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["engr1020"]

data = db["data"]
# have some identifier that is unique so that data will only appear once in the database
db.data.create_index([("Asset Identifier", pymongo.ASCENDING), ("Serial Number"), ("Location ID")], unique=True)
data.insert_many(df.to_dict(orient = 'records'), ordered = False)

# ping to confirm connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)