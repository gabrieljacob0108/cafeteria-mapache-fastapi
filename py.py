from pymongo import MongoClient

uri = "mongodb+srv://gabrieljacob:T1007158017@cluster0.w20wfrh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

print(client.list_database_names())
