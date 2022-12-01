import backend_functions as back
import requests
from urllib.parse import unquote
from urllib.parse import quote_plus

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = back.pymongo.MongoClient(link)
db = client["User"]
userCollection = db["Test"]

# import api
# debugUser = api.createPerson('debug')
#
# debugUser.dailyRecommender([60, 65, 63, "nothing"], "new")

match = userCollection.find({'username': 'forclothingaddition'})[0]

wardrobeLength = len(match['wardrobe'])
print(wardrobeLength)
url = 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-hoodie.jpg?alt=media&token=b761f8de-6679-42d4-a68d-f434e748dfb7'

body = {'username': 'forclothingaddition', 'lower': 60, 'upper': 65, 'url': url}
r = requests.post('https://outfit-forecast.herokuapp.com/classifyNew', json=body)

match = userCollection.find({'username': 'forclothingaddition'})[0]

wardrobeLength2 = len(match['wardrobe'])

print(wardrobeLength2)
