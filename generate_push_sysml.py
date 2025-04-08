from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from dotenv import load_dotenv
import os
from llm import generate_component_attributes, generate_sysml
import json

load_dotenv()

uri = os.getenv("DB_uri")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["engr1020"]

class_spec = db["component_class_spec"]

data = db["data"]
# generate sysml v2 textual class specification for a hardware component based on the names of the fields in db["data"]
if class_spec.count_documents({}) == 0:
    uml_class = generate_component_attributes(data.find_one().keys())
    class_spec.insert_one({"class_spec": uml_class})
else:
    uml_class = class_spec.find_one()["class_spec"]

print(uml_class)

# have some identifier that is unique so that data will only appear once in the database. then loop through the data and update with the new class spec
db.data.create_index([("Asset Identifier", pymongo.ASCENDING), ("Serial Number"), ("Location ID")], unique=True)
for doc in data.find():
    # check if the document has the "model" field
    if "model" not in doc:
        # update the document with the new class spec, generate a sysml v2 textual class specification for a hardware component based on the content of the document

        doc_copy = doc.copy()
        doc_copy['_id'] = str(doc_copy['_id'])

        uml_class = generate_sysml(json.dumps(doc_copy), uml_class)
        data.update_one({"_id": doc["_id"]}, {"$set": {"model": uml_class}})
