import backend_functions as back
import json

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

username = 'leo'
temp_min = '65'
temp_max = '60'
feels_like = '63'
atmosphere = 'cloudy'

match = userCollection.find({'username': username})[0]

wardrobeDict = match['wardrobe']
wardrobe = []
for item in wardrobeDict:
    newItem = back.Clothing(item['objectName'], item['classification'], item['imgURL'], item['clothingID'],
                            item['lowerTempBound'], item['upperTempBound'])
    wardrobe.append(newItem)

clothingHistoryDict = match['clothingHistory']
clothingHistory = []
for item in clothingHistoryDict:
    fit = []
    for i in range(4):
        fit.append(
            back.Clothing(item[i]['objectName'], item[i]['classification'], item[i]['imgURL'], item[i]['clothingID'],
                          item[i]['lowerTempBound'], item[i]['upperTempBound']))
    clothingHistory.append(fit)

currOutfitDict = match['currOutfit']
currOutfit = []
for item in currOutfitDict:
    newItem = back.Clothing(item['objectName'], item['classification'], item['imgURL'], item['clothingID'],
                            item['lowerTempBound'], item['upperTempBound'])
    currOutfit.append(newItem)

user = back.User(match['username'], wardrobe, clothingHistory, currOutfit, match['location'])

output = user.dailyRecommender([int(temp_min), int(temp_max), int(feels_like), atmosphere])
forJsonOutput = []
for elem in output:
    forJsonOutput.append(elem.__dict__)
print(json.dumps(forJsonOutput))
# user = back.User(match['username'], wardrobe, clothingHistory, currOutfit, match['location'])
#
# output = user.dailyRecommender([int(temp_min), int(temp_max), int(feels_like), atmosphere])
# forJsonOutput = []
# for elem in output:
#     forJsonOutput.append(elem.__dict__)
# return json.dumps(forJsonOutput)