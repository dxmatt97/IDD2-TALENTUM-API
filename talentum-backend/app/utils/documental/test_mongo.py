from pymongo import MongoClient

try:
    # Conexión al servidor local de MongoDB
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    db = client["test_db"]
    collection = db["test_collection"]

    # Insertar un documento de prueba
    result = collection.insert_one({"test": "mongo_ok"})

    # Leer el documento insertado
    doc = collection.find_one({"_id": result.inserted_id})
    print("MongoDB OK:", doc)
except Exception as e:
    print("MongoDB ERROR:", e)