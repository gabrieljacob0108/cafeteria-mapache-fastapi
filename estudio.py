import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://gabrieljacob:1007158017@cluster0.w20wfrh.mongodb.net/?appName=Cluster0")
db = cluster["test"]
collection = db["test"]

post1 = {"name": "tim", "score": 5}
post2 = {"name": "jason", "score": 8}
post3 = {"name": "dick", "score": 15}

collection.insert_many([post1, post2, post3])
results = collection.find({"name": {"$in": ["tim", "jason", "dick"]}})

for x in results:
    print("Hello, " + x["name"] + "!")