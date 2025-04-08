from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("DB_uri")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["engr1020"]

class_spec = db["component_class_spec"]

data = db["data"]

uml_class = class_spec.find_one()["class_spec"]

models = []
db.data.create_index([("Asset Identifier", pymongo.ASCENDING), ("Serial Number"), ("Location ID")], unique=True)
for doc in data.find():
    # check if the document has the "model" field
    if "model" in doc:
        # update the document with the new class spec, generate a sysml v2 textual class specification for a hardware component based on the content of the document
        models.append(doc["model"])

# create new temp folder
import os
import tempfile

temp_dir = tempfile.mkdtemp()
# print(f"Temporary directory created at: {temp_dir}")
# create a file in the temp folder
with open(os.path.join(temp_dir, "models.sysml"), "w") as f:
    # print(f"Writing models to {os.path.join(temp_dir, 'models.txt')}")
    f.write(uml_class + "\n")
    for model in models:
        f.write(model + "\n")

# print the path to the file
print(os.path.join(temp_dir, 'models.sysml'))
