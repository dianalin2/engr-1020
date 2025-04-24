from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from dotenv import load_dotenv
import os
from llm import generate_component_attributes, generate_sysml
import json

load_dotenv()

uri = os.getenv("DB_uri")

# create a new client and connect to the server
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

models = []
models_by_room = {}

# have some identifier that is unique so that data will only appear once in the database. then loop through the data and update with the new class spec
db.data.create_index([("Asset Identifier", pymongo.ASCENDING), ("Serial Number"), ("Location ID")], unique=True)

for doc in data.find():
    # check if the document has the "model" field
    if "model" in doc:
        # add the model to the list of models in the room
        if doc["Location ID"] not in models_by_room:
            models_by_room[doc["Location ID"]] = []
        models_by_room[doc["Location ID"]].append(doc["model"])

# create new folder for the models
import os
import datetime

dir = "../models/" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs(dir, exist_ok=True)

# create a file in the folder with the models for each room
with open(os.path.join(dir, "models.sysml"), "w") as f:
    # print(f"Writing models to {os.path.join(dir, 'models.txt')}")
    f.write(uml_class + "\n")
    for room, models in models_by_room.items():
        f.write(f"package {room} {{\n")
        for model in models:
            for line in model.splitlines():
                f.write(f"  {line}\n")
        f.write("}\n")

# save the model name to the database
model_collection = db["model"]
model_collection.create_index([("name", pymongo.ASCENDING)], unique=True)
model_collection.insert_one({"name": os.path.join(dir, 'models.sysml')})

# print the model name
print(os.path.join(dir, 'models.sysml'))


