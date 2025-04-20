from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from dotenv import load_dotenv
import os
import json
import html

load_dotenv()

uri = os.getenv("DB_uri")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["engr1020"]

class_spec = db["component_class_spec"]

data = db["data"]

all_assets = []
db.data.create_index([("Asset Identifier", pymongo.ASCENDING), ("Serial Number"), ("Location ID")], unique=True)
for doc in data.find():
    doc = doc.copy()
    doc['_id'] = str(doc['_id'])
    if 'last_modified' in doc:
        doc['last_modified'] = str(doc['last_modified'])
    # convert nans to None
    for key in doc.keys():
        if isinstance(doc[key], float) and (doc[key] != doc[key]):
            doc[key] = None

    all_assets.append(doc)

# print the json of all assets
print(json.dumps(all_assets))


