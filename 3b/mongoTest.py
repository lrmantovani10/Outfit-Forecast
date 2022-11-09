import backend_functions as back

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = back.pymongo.MongoClient(link)
db = client["User"]
collection = db["Test"]

username = 'leo'
match = collection.find({'username': username})[0]
# newClothing = back.Clothing("t-shirt", "topInner",
#                                "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7",
#                                'leo-0')
collection.update_one({'username' : username},{'$set': {'location': [39.057293, -94.577599]}})
#



# answers = collection.find({'username' : 'leo'})
#
# for elem in answers:
#     binary = elem['data']
#     user = pickle.loads(binary)
#     print(user.getUsername())