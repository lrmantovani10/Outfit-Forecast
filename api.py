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
    match = userCollection.find({'username': username})[0]

    user = back.User(match['username'], match['wardrobe'], match['clothingHistory'], match['currOutfit'], match['location'])

    output = user.dailyRecommender([int(temp_min), int(temp_max), int(feels_like), atmosphere])
    forJsonOutput = []
    for elem in output:
        forJsonOutput.append(elem.__dict__)
    return json.dumps(forJsonOutput)

@app.route('/classifyNew/<username>/<URL>/<lower>/<upper>')
def classifyNew(username, URL, lower, upper):
    match = userCollection.find({'username': username})[0]

    user = back.User(match['username'], match['wardrobe'], match['clothingHistory'], match['currOutfit'], match['location'])

    # Returns a status string (like below)
    return user.classifyNew(URL, lower, upper)

@app.route('/createUser/<username>')
def createUser(username):
    match = list(userCollection.find({'username': username}))
    if len(match) == 0:
        newUser = back.User("", [], [], [], [])
        newUser.setUsername(username)
        newInsert = {"username": username, "wardobe" : [], "clothingHistory" : [], "currOutfit" : [], "location" : []}
        userCollection.insert_one(newInsert)
        return "User created"
    return "Username taken"

if __name__ == '__main__':
    app.run()