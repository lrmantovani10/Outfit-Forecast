from flask import Flask
import backend_functions as back
import json

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = back.pymongo.MongoClient(link)
userDB = client["User"]
userCollection = userDB["Test"]

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return "<h1> Deployed to Heroku</h1>"

@app.route('/dailyRecommender/<username>/<temp_min>/<temp_max>/<feels_like>/<atmosphere>')
def dailyRecommender(username, temp_min, temp_max, feels_like, atmosphere):
    try:
        match = userCollection.find({'username': username})[0]
    except:
        return "Invalid username"
    
    wardrobeDict = match['wardrobe']
    wardrobe = []
    for item in wardrobeDict:
        newItem = back.Clothing(item['objectName'], item['classification'], item['imgURL'], item['clothingID'], item['lowerTempBound'], item['upperTempBound'])
        wardrobe.append(newItem)
        
    clothingHistoryDict = match['clothingHistory']
    clothingHistory = []
    for item in clothingHistoryDict:
        fit = []
        for i in range(4):
            fit.append(back.Clothing(item[i]['objectName'], item[i]['classification'], item[i]['imgURL'], item[i]['clothingID'], item[i]['lowerTempBound'], item[i]['upperTempBound']))
        clothingHistory.append(fit)
        
    currOutfitDict = match['currOutfit']
    currOutfit = []
    for item in currOutfitDict:
        newItem = back.Clothing(item['objectName'], item['classification'], item['imgURL'], item['clothingID'], item['lowerTempBound'], item['upperTempBound'])
        currOutfit.append(newItem)
    
    user = back.User(match['username'], wardrobe, clothingHistory, currOutfit, match['location'])

    output = user.dailyRecommender([int(temp_min), int(temp_max), int(feels_like), atmosphere])
    forJsonOutput = []
    for elem in output:
        forJsonOutput.append(elem.__dict__)
    return json.dumps(forJsonOutput)

@app.route('/classifyNew/<username>/<URL>/<lower>/<upper>')
def classifyNew(username, URL, lower, upper):
    match = userCollection.find({'username': username})[0]
    
    wardrobeDict = match['wardrobe']
    wardrobe = []
    for item in wardrobeDict:
        newItem = Clothing(item['objectName'], item['classification'], item['imgURL'], item['clothingID'], item['lowerBound'], item['upperBound'])
        wardrobe.append(newItem)
        
    clothingHistoryDict = match['clothingHistory']
    clothingHistory = []
    for item in clothingHistoryDict:
        fit = []
        for i in range(4):
            fit.append(Clothing(item[i]['objectName'], item[i]['classification'], item[i]['imgURL'], item[i]['clothingID'], item[i]['lowerBound'], item[i]['upperBound']))
        clothingHistory.append(fit)
        
    currOutfitDict = match['currOutfit']
    currOutfit = []
    for item in currOutfitDict:
        newItem = Clothing(item['objectName'], item['classification'], item['imgURL'], item['clothingID'], item['lowerBound'], item['upperBound'])
        currOutfit.append(newItem)
    
    user = back.User(match['username'], wardrobe, clothingHistory, currOutfit, match['location'])

    # Returns a status string (like below)
    return user.classifyNew(URL, lower, upper)

@app.route('/createUser/<username>')
def createUser(username):
    match = list(userCollection.find({'username': username}))
    if len(match) == 0:
        newUser = back.User("", [], [], [], [])
        if (newUser.setUsername(username)):
            newInsert = {"username": username, "wardobe" : [], "clothingHistory" : [], "currOutfit" : [], "location" : []}
            userCollection.insert_one(newInsert)
            return "User created"
        else:
            return "Username does not meet requirements"
    return "Username taken"

if __name__ == '__main__':
    app.run()
