import backend_functions as back

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = back.pymongo.MongoClient(link)
db = client["User"]
collection = db["Test"]

username = 'leo'
user = back.User(username, [], [], [], [])

test = {"username": username, "wardobe" : [], "clothingHistory" : [], "currOutfit" : [], "location" : []}

collection.insert_one(test)

# answers = collection.find({'username' : 'leo'})
#
# for elem in answers:
#     binary = elem['data']
#     user = pickle.loads(binary)
#     print(user.getUsername())