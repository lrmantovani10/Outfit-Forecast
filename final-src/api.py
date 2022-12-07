from flask import Flask, request
import backend_functions as back
import json
from urllib.parse import unquote_plus

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = back.pymongo.MongoClient(link)
userDB = client["User"]
userCollection = userDB["Test"]

app = Flask(__name__)
app.config["DEBUG"] = True

# helper
def createPerson(username):
    try:
        match = userCollection.find({'username': username})[0]
    except:
        return "Invalid username"

    wardrobeDict = match['wardrobe']
    wardrobe = []
    for item in wardrobeDict:
        try:
            newItem = back.Clothing(item['objectName'], item['objectNames'], item['classification'], item['imgURL'], item['clothingID'],
                                    item['lowerTempBound'], item['upperTempBound'])
        except:
            newItem = None
        wardrobe.append(newItem)

    clothingHistoryDict = match['clothingHistory']
    clothingHistory = []
    for item in clothingHistoryDict:
        fit = []
        for i in range(4):
            try:
                fit.append(back.Clothing(item[i]['objectName'], item[i]['objectNames'], item[i]['classification'], item[i]['imgURL'],
                                         item[i]['clothingID'], item[i]['lowerTempBound'], item[i]['upperTempBound']))
            except:
                fit.append(None)
        clothingHistory.append(fit)

    currOutfitDict = match['currOutfit']
    currOutfit = []
    for item in currOutfitDict:
        try:
            newItem = back.Clothing(item['objectName'], item['objectNames'], item['classification'], item['imgURL'], item['clothingID'],
                                    item['lowerTempBound'], item['upperTempBound'])
        except:
            newItem = None
        currOutfit.append(newItem)

    queueDict = match['outfitQueue']
    outfitQueue = []
    for item in queueDict:
        fit = []
        for i in range(4):
            try:
                fit.append(back.Clothing(item[i]['objectName'], item[i]['objectNames'], item[i]['classification'], item[i]['imgURL'],
                                         item[i]['clothingID'], item[i]['lowerTempBound'], item[i]['upperTempBound']))
            except:
                fit.append(None)
        outfitQueue.append(fit)

    return back.User(match['username'], wardrobe, clothingHistory, currOutfit, outfitQueue, match['queueIndex'], match['location'])

@app.route('/')
def index():
    return "<h1> Deployed to Heroku</h1>"

@app.route('/dailyRecommender/<username>/<temp_min>/<temp_max>/<feels_like>/<atmosphere>/<callStatus>')
def dailyRecommender(username, temp_min, temp_max, feels_like, atmosphere, callStatus):
    user = createPerson(username)
    if user == "Invalid username":
        return "Invalid username"

    output = user.dailyRecommender([int(temp_min), int(temp_max), int(feels_like), atmosphere], callStatus)
    forJsonOutput = []
    for elem in output:
        try:
            forJsonOutput.append(elem.__dict__)
        except:
            forJsonOutput.append(None)
    return json.dumps(forJsonOutput)


@app.route('/classifyNew', methods=['POST'])
def classifyNew():
    username = request.json['username']
    lower = request.json['lower']
    upper = request.json['upper']
    url = request.json['url']

    user = createPerson(username)
    if user == "Invalid username":
        return "Invalid username"
    # Returns a status string (like below)
    output = user.classifyNew(url, lower, upper, True)
    return json.dumps(output)

@app.route('/createUser/<username>')
def createUser(username):
    match = list(userCollection.find({'username': username}))
    if len(match) == 0:
        newUser = back.User("", [], [], [], [], 0, [])
        if (newUser.setUsername(username)):
            newInsert = {"username": username, "wardrobe" : [], "clothingHistory" : [], "currOutfit" : [], "outfitQueue" : [], "queueIndex" : 0, "location" : []}
            userCollection.insert_one(newInsert)
            return "User created"
        else:
            return "Username does not meet requirements"
    return "Username taken"

if __name__ == '__main__':
    app.run()
