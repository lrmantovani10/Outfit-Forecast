import pymongo

class User:
    def __init__(self, username):
        self.username = username
        self.wardrobe = []
        self.clothingHistory = []
        self.currOutfit = []
        self.location = ()

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
    def setUsername(self, username):
        valid = False
        #isalnum checks that it doesn't have whitespaces or special characters
        if username.length() <= 32 and username.length > 0 and username.isalnum():
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

    # must be of type
    def setLocation(self, locArr):
        return True       
    
    # outfit must be a list of clothing items
    def updateClothingHistory(self, outfit):
        if type(outfit) is list:
            for x in outfit:
                if type(x) is not Clothing:
                    return False
            self.clothingHistory.append(outfit)
            return True   
        else:
            return False


    # ------- ------- ------- ------- -------
    
    def classifyNew(self, imgURL):
        return True


class Clothing:
    def __init__(self, name, imgURL, clothingID):
        self.objectName = name
        self.warmthRating = 0
        self.clothingID = clothingID
        self.classification = ""
        self.imgURL = imgURL

    # ------- getters -------
    def getObjectName(self):
        return self.objectName

    def getWarmthRating(self):
        return self.warmthRating

    def getClothingID(self):
        return self.clothingID
    
    def getClassification(self):
        return self.classification

    def getImgURL(self):
        return self.imgURL
    
    # ------- getters -------
    def setObjectName(self, name):
        return True

    def setWarmthRating(self, value):
        return True
    
    def setClassification(self, name):
        return True


class EnviornmentalData:
    def __init__(self):
        newUser = User("")
        self.enviroData = newUser
        
    def getWeather():
        return []



