import pymongo
from pymongo import MongoClient

def test_connection():   
    cluster = MongoClient("mongodb+srv://DGilb23:Bhhe2nsBOXwI4Axh@cluster0.mpb6ff1.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["Clothing"]
    collection = db["Test"]
    test = {"username": "Test Success"}
    collection.insert_one(test)
    print("Connection Successful!")

test_connection()