from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from dotenv import load_dotenv
from bson import ObjectId
import os
import json
import sys
import datetime

load_dotenv()

uri = os.getenv("DB_uri")

id = sys.argv[1]
new_model = sys.argv[2]

# create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["engr1020"]

class_spec = db["component_class_spec"]

data = db["data"]

db.data.create_index([("Asset Identifier", pymongo.ASCENDING), ("Serial Number"), ("Location ID")], unique=True)

# update the document with the new class spec that was passed in
data.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"model": new_model, "last_modified": datetime.datetime.now()}})
