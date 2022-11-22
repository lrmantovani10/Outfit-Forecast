import os
import math
from google.cloud import vision
from google.cloud.vision_v1 import types
import pymongo

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'inspiring-list-367201-258ee5841906.json'

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = pymongo.MongoClient(link)
userDB = client["User"]
userCollection = userDB["Test"]

# only user setters need to access and modify db
class User:
    def __init__(self, username, wardrobe, clothingHistory, currOutfit, outfitQueue, queueIndex, location):
        # realized duplicate username check do not need to happen here, only on front-end route where the user is originally created
        self.username = ""
        self.setUsername(username)

        self.wardrobe = wardrobe
        self.clothingHistory = clothingHistory

        self.currOutfit = []
        self.setCurrOutfit(currOutfit)

        self.outfitQueue = outfitQueue
        self.queueIndex = queueIndex

        self.location = []
        self.setLocation(location)

    # ------- getters -------
    def getUsername(self):
        return self.username
    
    def getWardrobe(self):
        return self.wardrobe

    def getLocation(self):
        return self.location 

    def getCurrOutfit(self):
        return self.currOutfit   

    def getClothingHistory(self):
        return self.clothingHistory   

    def getOutfitQueue(self):
        return self.outfitQueue

    def getQueueIndex(self):
        return self.queueIndex

    # -------  setters  -------
    ''' 
    - must be at most 32 characters
    - cannot be empty
    - must have at least one letter
    - can't start with number
    - must be alphanumeric (no whitespaces or special characters)
    '''

    # user can't change their username, this is for internal use only
    def setUsername(self, username):
        valid = False
        #isalnum checks that it doesn't have whitespaces or special characters
        if len(username) <= 32 and len(username) > 0 and username.isalnum():
            #can't be all digits, can't start with a digit
            if username.isdigit() or username[0].isdigit():
                return False
            for c in username:
                if c.isalpha(): #has at least one letter
                    valid = True
                    break
        if valid:
            self.username = username
            return True
        else:
            return False

    # must be of type clothing
    def updateWardrobe(self, clothingItem, db = True):
        if type(clothingItem) is Clothing:
            self.wardrobe.append(clothingItem)
            if db:
                userCollection.update_one({'username': self.getUsername()}, {'$push': {'wardrobe': clothingItem.__dict__}})
            return True
        else:
            return False

    # must be of type [latitude, longitude]
    def setLocation(self, locArr, db = True):
        if len(locArr) == 2:
            if locArr[0]>= -90 and locArr[0] <= 90 and locArr[1] >= -180 and locArr[1] <= 180:
                self.location = locArr
                if db:
                    userCollection.update_one({'username' : self.getUsername()},{'$set': {'location': locArr}})
                return True
            else:
                return False
        return False

    # outfit must be a list of 4 clothing items
    def updateClothingHistory(self, outfit, db = True):
        if type(outfit) is list:
            if (len(outfit) != 4):
                return False
            for x in outfit:
                if type(x) is not Clothing:
                    return False
            self.clothingHistory.append(outfit)
            if db:
                outfitDict = []
                for item in outfit:
                    outfitDict.append(item.__dict__)
                userCollection.update_one({'username': self.getUsername()}, {'$push': {'clothingHistory': outfitDict}})
            return True   
        else:
            return False
    
    # outfit must be a list of 4 clothing items
    def setCurrOutfit(self, outfit, db = True):
        if type(outfit) is list:
            if (len(outfit) != 4):
                return False
            for x in outfit:
                if type(x) is not Clothing:
                    return False
            self.currOutfit = outfit
            if db:
                outfitDict = []
                for item in outfit:
                    outfitDict.append(item.__dict__)
                userCollection.update_one({'username' : self.getUsername()},{'$set': {'currOutfit': outfitDict}})
            return True   
        else:
            return False

    def setQueueIndex(self, index, db = True):
        if type(index) is not int:
            return False
        self.queueIndex = index
        if db:
            userCollection.update_one({'username': self.getUsername()}, {'$set': {'queueIndex': index}})
        return True

    def setOutfitQueue(self, newQueue, db = True):
        if type(newQueue) is list:
            for x in newQueue:
                if len(x) != 4:
                    return False
                for y in x:
                    if type(y) is not Clothing:
                        return False
            self.outfitQueue = newQueue
            if db:
                newQueueDict = []
                for outfit in newQueue:
                    outfitDict = []
                    for item in outfit:
                        outfitDict.append(item.__dict__)
                    newQueueDict.append(outfitDict)
                userCollection.update_one({'username': self.getUsername()}, {'$set': {'outfitQueue': newQueueDict}})
            return True
        else:
            return False

    def popClothingHistory(self, db = True):
        self.clothingHistory.pop(-1)
        if db:
            userCollection.update_one({'username': self.getUsername()}, {'$pop': {'clothingHistory': 1}})
        return True


    # ------- ------- ------- ------- -------
    
    '''
    call google vision api on imgURL to get back classification
    parse classification (preset categories and if it falls in one of those you take it)
    create clothing item
    call updateWardrobe on that clothing item
    '''
    def classifyNew(self, imgURL, lower, upper, db = True):
        topOuter = ['jacket', 'sweater', 'coat', 'sweatshirt', 'outerwear']
        topInner = ['t-shirt', 'shirt', 'dress', 'sleeveless shirt', 'top']
        bottom = ['jeans', 'shorts', 'pants', 'skirt']
        shoes = ['shoe', 'footwear', 'sneakers', 'boots', 'heels']

        client = vision.ImageAnnotatorClient()
        image = types.Image()
        image.source.image_uri = imgURL
        classification_label = client.object_localization(image=image)
        response_label = client.label_detection(image=image)
        
        if 'error' in response_label or 'error' in classification_label:
            return "API Error"

        found = False
        temp = ""
        name = ""
        classification = ""
        username = self.getUsername() + "-" + str(len(self.getWardrobe()))

        for label in classification_label.localized_object_annotations:
            temp = label.name.lower()
            if temp in topOuter:
                classification = "topOuter"
                found = True
                break
            if temp in topInner:
                classification = "topInner"
                found = True
                break
            if temp in bottom:
                classification = "bottom"
                found = True
                break
            if temp in shoes:
                classification = "shoes"
                found = True
                break
        
        if found == False:
            return "Could not classify the Image"

        name = temp
        newItem = Clothing(name, classification, imgURL, username, lower, upper)
        self.updateWardrobe(newItem, db)
        return "Image Classified: " + name

    def dailyRecommender(self, weatherInput, callStatus, db = True):
        if callStatus == "reject":
            # no need to run a new prediction
            queueIndex = self.getQueueIndex()
            outfitQueue = self.getOutfitQueue()

            self.popClothingHistory(db)
            if queueIndex == len(outfitQueue) - 1:
                queueIndex = 0
            else:
                queueIndex += 1

            self.updateClothingHistory(outfitQueue[queueIndex], db)
            self.setCurrOutfit(outfitQueue[queueIndex], db)
            self.setQueueIndex(queueIndex, db)
            return outfitQueue[queueIndex]

        if callStatus == "new":
            # weatherInput format: ["temp_min", "temp_max", "feels_like", "atmosphere"]
            temp_min = weatherInput[0]
            temp_max = weatherInput[1]
            feels_like = weatherInput[2]
            atmosphere = weatherInput[3]

            minTopOuterRange = math.inf
            minTopOuterRange2 = math.inf

            minTopInnerRange = math.inf
            minTopInnerRange2 = math.inf

            minBottomRange = math.inf
            minBottomRange2 = math.inf

            minShoesRange = math.inf
            minShoesRange2 = math.inf

            topOuterConditionsMet = False
            topInnerConditionsMet = False
            bottomConditionsMet = False
            shoesConditionsMet = False

            output = [None, None, None, None]
            output2 = [None, None, None, None]

            # CURRENT ALGORITHM: CHOOSES CLOTHING ITEM WITH TIGHTEST (SMALLEST) SURVEY TEMPERATURE RANGE
            # WHERE THE DAILY MAX AND MIN TEMPERATURES FALL INTO THAT RANGE

            # accounts for some atmosphere conditions
            # will never recommend outer top for feels_like >= 75

            for item in self.getWardrobe():
                lower = item.getLowerBound()
                upper = item.getUpperBound()
                if not (lower <= temp_min <= upper and lower <= temp_max <= upper):
                    continue
                rangeF = upper - lower
                if item.classification == "topOuter":
                    if feels_like >= 75:
                        continue
                    if 'rain' in atmosphere or 'snow' in atmosphere:
                        if 'jacket' not in item.getObjectName() and 'coat' not in item.getObjectName() and 'wind' not in item.getObjectName() and 'parka' not in item.getObjectName() and 'rain' not in item.getObjectName() and 'snow' not in item.getObjectName():
                            if topOuterConditionsMet:
                                continue
                        else:
                            if not topOuterConditionsMet:
                                topOuterConditionsMet = True
                                output[0] = item
                                minTopOuterRange = rangeF

                    if rangeF < minTopOuterRange:
                        output2[0] = output[0]
                        output[0] = item
                        minTopOuterRange2 = minTopOuterRange
                        minTopOuterRange = rangeF
                    elif rangeF < minTopOuterRange2:
                        output2[0] = item
                        minTopOuterRange2 = rangeF
                if item.classification == "topInner":
                    # no topInnerConditions yet, might add short/long sleeve in the future
                    if rangeF < minTopInnerRange:
                        output2[1] = output[1]
                        output[1] = item
                        minTopInnerRange2 = minTopInnerRange
                        minTopInnerRange = rangeF
                    elif rangeF < minTopInnerRange2:
                        output2[1] = item
                        minTopInnerRange2 = rangeF
                if item.classification == "bottom":
                    if 'rain' in atmosphere or 'snow' in atmosphere:
                        if 'short' in item.getObjectName():
                            if bottomConditionsMet:
                                continue
                        else:
                            if not bottomConditionsMet:
                                bottomConditionsMet = True
                                output[2] = item
                                minBottomRange = rangeF

                    if rangeF < minBottomRange:
                        output2[2] = output[2]
                        output[2] = item
                        minBottomRange2 = minBottomRange
                        minBottomRange = rangeF
                    elif rangeF < minBottomRange2:
                        output2[2] = item
                        minBottomRange2 = rangeF

                if item.classification == "shoes":
                    if 'rain' in atmosphere or 'snow' in atmosphere:
                        if 'boot' not in item.getObjectName() and 'rain' not in item.getObjectName() and 'snow' not in item.getObjectName():
                            if shoesConditionsMet:
                                continue
                        else:
                            if not shoesConditionsMet:
                                shoesConditionsMet = True
                                output[3] = item
                                minShoesRange = rangeF

                    if rangeF < minShoesRange:
                        output2[3] = output[3]
                        output[3] = item
                        minShoesRange2 = minShoesRange
                        minShoesRange = rangeF
                    elif rangeF < minShoesRange2:
                        output2[3] = item
                        minShoesRange2 = rangeF

            # Adds combinations of outfits 1 and 2 to the queue
            queueIndex = 0
            outfitQueue = []

            outfitQueue.append(output)

            for i in range(4):
                if output2[i] != None:
                    outfitQueue.append(output[:i] + output2[i] + output[i+1:])

            for i in range(4):
                if output2[i] != None:
                    for j in range(i+1,4):
                        if output2[j] != None:
                            newOutput = output
                            newOutput[i] = output2[i]
                            newOutput[j] = output2[j]
                            outfitQueue.append(newOutput)

            for i in range(4):
                newOutput = output2
                newOutput[i] = output[i]
                if None not in newOutput[:i] and None not in newOutput[i+1:]:
                    outfitQueue.append(newOutput)

            outfitQueue.append(output2)
            outfitQueue = list(set(outfitQueue))

            # don't suggest yesterday's chosen outfit
            if len(outfitQueue) != 1:
                if self.getClothingHistory()[-1] in outfitQueue:
                    outfitQueue.remove(self.getClothingHistory()[-1])

            # Sets/returns first outfit and updates history with it
            self.updateClothingHistory(outfitQueue[0], db)
            self.setCurrOutfit(outfitQueue[0], db)

            self.setQueueIndex(queueIndex, db)
            self.setOutfitQueue(outfitQueue, db)
            return outfitQueue[0] # still returns first outfit, but sets up multiple
        else:
            return "Invalid call status (must be new/reject)"

class Clothing:
    def __init__(self, name, classification, imgURL, clothingID, lowerBound = -20, upperBound = 120):
        self.objectName = ""
        self.setObjectName(name)

        self.classification = ""
        self.setClassification(classification)
        
        self.clothingID = clothingID
        self.imgURL = imgURL

        self.lowerTempBound = -20
        self.upperTempBound = 120
        self.setBounds(lowerBound, upperBound)

    # ------- getters -------
    def getObjectName(self):
        return self.objectName

    def getClothingID(self):
        return self.clothingID
    
    def getClassification(self):
        return self.classification

    def getImgURL(self):
        return self.imgURL
    
    def getLowerBound(self):
        return self.lowerTempBound
    
    def getUpperBound(self):
        return self.upperTempBound
    
    # ------- setters -------

    # assume that the setters are called once by classifyNew and never again (below)
    def setBounds(self, lower, upper = 1000):
        if -20 <= lower <= 120 and -20 <= upper <= 120:
            self.lowerTempBound = lower
            self.upperTempBound = upper
            return True
        return False

    def setObjectName(self, name):
        if isinstance(name, str) and name != "" and any(c.isalpha() for c in name):
            self.objectName = name
            return True
        return False

    def setClassification(self, name):
        if name == "topOuter" or name == "topInner" or name == "bottom" or name == "shoes":
            self.classification = name
            return True
        return False