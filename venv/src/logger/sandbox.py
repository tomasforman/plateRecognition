from pymongo import MongoClient

client = MongoClient()
db = client["test"]
plates = db["logs"]

plate = {
    "timestamp": "today",
    "plate": "AD128LY",
    "url": "lala.com/"
}
plates.insert_one(plate)