import backend_functions as back

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = back.pymongo.MongoClient(link)
db = client["User"]
userCollection = db["Test"]

# user = back.User("leo", [], [], [], [])
# top1 = back.Clothing("sweater", "topOuter",
#                                "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-sweater.jpg?alt=media&token=ded9d625-062e-4e61-bbdc-a3988104fb8b",
#                                'leo-0')
# top2 = back.Clothing("t-shirt", "topInner",
#                                "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7",
#                                'leo-1')
# bottom = back.Clothing("sweatpants", "bottom",
#                                "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-sweatpants.jpg?alt=media&token=9c54025f-94f1-4759-9894-6df682867241",
#                                'leo-2')
# shoes = back.Clothing("shoes", "shoes",
#                                "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shoes.jpg?alt=media&token=a1f187f2-ca97-41b2-a39f-8291f34849bd",
#                                'leo-3')
#
# user.updateWardrobe(top1)
# user.updateWardrobe(top2)
# user.updateWardrobe(bottom)
# user.updateWardrobe(shoes)

# Removes last element from array
# userCollection.update_one({'username': 'leo'}, {'$pop': {'clothingHistory': -1}})