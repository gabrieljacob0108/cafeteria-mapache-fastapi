from pymongo import MongoClient

uri = "mongodb+srv://gabrieljacob:1007158017@cluster0.w20wfrh.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)

db = client["tienda"]
coleccion = db["productos"]


coleccion.insert_one({"nombre": "final_test"})

print("✅ todo funciona limpio")

