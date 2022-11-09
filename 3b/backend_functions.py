import os
from google.cloud import vision
from google.cloud.vision_v1 import types
import pymongo
from bson.binary import Binary
# from zoneinfo import ZoneInfo

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'inspiring-list-367201-258ee5841906.json'

link = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"

client = pymongo.MongoClient(link)
userDB = client["User"]
userCollection = userDB["Test"]

# only user setters need to access and modify db
class User:
    def __init__(self, username, wardrobe, clothingHistory, currOutfit, location):
        # realized duplicate username check do not need to happen here, only on front-end route where the user is originally created
        self.username = username
        self.wardrobe = wardrobe
        self.clothingHistory = clothingHistory
        self.currOutfit = currOutfit
        self.location = location

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

    # -------  setters  -------
    ''' 
    - must be at most 32 characters
    - cannot be empty
    - must have at least one letter
    - can't start with number
    - must be alphanumeric (no whitespaces or special characters)
    '''

    # user can't change their username, this is for internal use
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
    def updateWardrobe(self, clothingItem):
        if type(clothingItem) is Clothing:
            self.wardrobe.append(clothingItem)
            return True
        else:
            return False

    # must be of type [latitude, longitude]
    def setLocation(self, locArr):
        if len(locArr) == 2:
            if locArr[0]>= -90 and locArr[0] <= 90 and locArr[1] >= -180 and locArr[1] <= 180:
                self.location = locArr
                return True
            else:
                return False
        return False

    # outfit must be a list of 4 clothing items
    def updateClothingHistory(self, outfit):
        if type(outfit) is list:
            if (len(outfit) != 4):
                return False
            for x in outfit:
                if type(x) is not Clothing:
                    return False
            self.clothingHistory.append(outfit)
            return True   
        else:
            return False
    
    # outfit must be a list of 4 clothing items
    def setCurrOutfit(self, outfit):
        if type(outfit) is list:
            if (len(outfit) != 4):
                return False
            for x in outfit:
                if type(x) is not Clothing:
                    return False
            self.currOutfit = outfit
            return True   
        else:
            return False


    # ------- ------- ------- ------- -------
    
    '''
    call google vision api on imgURL to get back classification
    parse classification (preset categories and if it falls in one of those you take it)
    create clothing item
    call updateWardrobe on that clothing item

    '''
    def classifyNew(self, imgURL, lower, upper):
        topOuter = ['jacket', 'sweater', 'coat', 'hoodie']
        topInner = ['t-shirt', 'shirt']
        bottoms = ['jeans', 'shorts', 'pants', 'skirt']
        shoes = ['shoe', 'footwear', 'sneakers', 'boots', 'heels']

        client = vision.ImageAnnotatorClient()
        image = types.Image()
        image.source.image_uri = imgURL
        response_label = client.label_detection(image=image)
        found = False
        if 'error' in response_label:
            return "API Error"
        for label in response_label.label_annotations:
            lab = label.description.lower()
            if lab in topOuter:
                newItem = Clothing(lab, "topOuter", imgURL, self.getUsername() + "_" + str(len(self.getWardrobe())), lower, upper)
                found = True
                break
            elif lab in topInner: 
                newItem = Clothing(lab, "topInner", imgURL, self.getUsername() + "_" + str(len(self.getWardrobe())), lower, upper)
                found = True
                break
            elif lab in bottoms: 
                newItem = Clothing(lab, "bottom", imgURL, self.getUsername() + "_" + str(len(self.getWardrobe())), lower, upper)
                found = True
                break
            elif lab in shoes: 
                newItem = Clothing(lab, "shoes", imgURL, self.getUsername() + "_" + str(len(self.getWardrobe())), lower, upper)
                found = True
                break
        if found == False:
            return "Could not classify the Image"
        self.updateWardrobe(newItem)
        return "Image Classified: " + lab

    def dailyRecommender(self, weatherInput):
        # weatherInput format: ["temp_min", "temp_max", "feels_like", "atmosphere"]
        temp_min = weatherInput[0]
        temp_max = weatherInput[1]
        feels_like = weatherInput[2]
        atmosphere = weatherInput[3]

        minTopOuterRange = math.inf
        minTopInnerRange = math.inf
        minBottomRange = math.inf
        minShoesRange = math.inf

        topOuterConditionsMet = False
        topInnerConditionsMet = False
        bottomConditionsMet = False
        shoesConditionsMet = False

        output = [None, None, None, None]

        # CURRENT ALGORITHM: CHOOSES CLOTHING ITEM WITH TIGHTEST (SMALLEST) SURVEY TEMPERATURE RANGE
        # WHERE THE DAILY MAX AND MIN TEMPERATURES FALL INTO THAT RANGE

        # accounts for some atmosphere conditions
        # will never recommend outer top for feels_like >= 75

        for item in self.getWardrobe():
            lower = item.getLowerBound()
            upper = item.getUpperBound()
            if not (lower <= temp_min <= upper and lower <= temp_max <= upper):
                continue
            range = upper - lower
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
                            minTopOuterRange = range

                if range <= minTopOuterRange:
                    output[0] = item
                    minTopOuterRange = range
            if item.classification == "topInner":
                # no topInnerConditions yet, might add short/long sleeve in the future
                if range <= minTopInnerRange:
                    output[1] = item
                    minTopInnerRange = range
            if item.classification == "bottom":
                if 'rain' in atmosphere or 'snow' in atmosphere:
                    if 'short' in item.getObjectName():
                        if bottomConditionsMet:
                            continue
                    else:
                        if not bottomConditionsMet:
                            bottomConditionsMet = True
                            output[2] = item
                            minBottomRange = range

                if range <= minBottomRange:
                    output[2] = item
                    minBottomRange = range
            if item.classification == "shoes":
                if 'rain' in atmosphere or 'snow' in atmosphere:
                    if 'boot' not in item.getObjectName() and 'rain' not in item.getObjectName() and 'snow' not in item.getObjectName():
                        if shoesConditionsMet:
                            continue
                    else:
                        if not shoesConditionsMet:
                            shoesConditionsMet = True
                            output[3] = item
                            minShoesRange = range

                if range <= minShoesRange:
                    output[3] = item
                    minShoesRange = range
        self.clothingHistory.append(output)
        self.currOutfit = output
        return output

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
    def setBounds(self, lower, upper):
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
