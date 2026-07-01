from bson import ObjectId
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

load_dotenv(".env")

password = os.environ.get("MONGODB_PWD")

connection_string =f"mongodb+srv://gabrieljacob:{password}@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"

client = MongoClient(connection_string)
pprint.pprint(client.list_database_names())
dbs = client.list_database_names()
test_db = client.test
collections = test_db.list_collection_names()
pprint.pprint(collections)

def insert_test_doc():
    collection = test_db.test
    test_document = {
        "name": "tim", 
        "last_name": "timberton",
        }
    insert_id = collection.insert_one(test_document)
    print("Inserted ID:", insert_id.inserted_id)
production = client.production
person_collection = production.person_collection

def create_documents():
    first_names = ["Tim", "Sarah", "Jennifer", "Jose", "Brad", "Allen"]
    last_names = ["Ruscica", "Smith", "Bart", "Cater", "Pit", "Geral"]
    ages = [21, 40, 23, 19, 34, 67]

    docs = []

    for first_name, last_name, age in zip(first_names, last_names, ages):
        doc = {"first_name": first_name, "last_name": last_name, "age": age}
        docs.append(doc)

    person_collection.insert_many(docs)

#create_documents() 

def find_all_people():
    people = person_collection.find()
    printer = pprint.PrettyPrinter()
    for person in people:
        printer.pprint(person) 
        
def get_person_by_id(person_id):
    from bson import ObjectId
    printer = pprint.PrettyPrinter()  # ← agrégala aquí
    id_ = ObjectId(person_id)
    person = person_collection.find_one({"_id": id_})
    printer.pprint(person)
def get_age_range(min_age, max_age):
    import pprint
    printer = pprint.PrettyPrinter()

    query = {
        "age": {
            "$gte": min_age,
            "$lte": max_age
        }
    }

    people = person_collection.find(query).sort("age")

    for person in people:
        printer.pprint(person)
    
def update_person_by_id(person_id):
    from bson.objectid import ObjectId
    printer = pprint.PrettyPrinter()
    _id = ObjectId(person_id)
    
    all_updates = {
        "$set": {"new_field": True},
        "$inc": {"age": 1},
        "$rename": {"first_name": "first", "last_name": "last"}
    }
    person_collection.update_one({"_id": _id}, all_updates)
    person = person_collection.find_one({"_id": _id})
    printer.pprint(person)
def delete_doc_by_id(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    person_collection.delete_one({"_id": _id})

    

delete_doc_by_id("6a281e4eeaef5995b9d9b3a0")
address = {
    "_id": "62475964011a9126a4cebeb7",
    "street": "Bay Street",
    "number": 2706,
    "city": "San Francisco",
    "country": "United States",
    "zip": "94107"
}
def add_address_embed(person_id, address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    person_collection.update_one(
        {"_id": _id}, {"$addToSet": {'addresses': address}})

def add_address_relationship(person_id, address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

person = {"_id": "62475964011a9126a4"}
def add_address_relationship(person_id, address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    address = address.copy()
    address["owner_id"] = person_id

    address_collection = production.address
    address_collection.insert_one(address)

add_address_relationship("62475964011a9126a4cebeb8", address)



        


                        
    
    
