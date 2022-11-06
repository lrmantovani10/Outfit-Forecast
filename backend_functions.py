import pymongo

class User:
    def __init__(self, username):
        self.username = username
        self.wardrobe = []
        self.clothingHistory = []
        self.preferences = []
        self.currOutfit = []
        #self.location = 

    def getUsername(self):
        return self.username

    ''' 
    - must be at most 32 characters
    - cannot be empty
    - must have at least one letter and one number
    - can't start with number
    - can't have special characters 
    '''
    def setUsername(self, username):
        if username.length() <= 32 and username.length > 0 and hasLetter(username) and hasDigit(username) and !username[0].isdigit() and !hasSpecial(username):
            self.username = username
            return True
        else:
            return False

    def getWardrobe(self):
        return self.wardrobe

    def updateWardrobe(self, clothingItem):
        if type(clothingItem) is Clothing:
            self.wardrobe.append(clothingItem)
            return True
        else:
            return False

    def setPreference(self, prefArr):
        return True

    def getPreferences(self):
        return self.preferences
    
    def setLocation(self, locArr):
        return True   
    
    def getLocation(self):
        return self.location         
    
    def getCurrOutfit(self):
        return self.currOutfit          
    
    '''
    need to make sure outfit is a list of clothing items
    '''
    def updateClothingHistory(self, outfit):
        return True   
    
    def getClothingHistory(self):
        return self.clothingHistory         

    def classifyNew(self, imgURL):
        return    


class Clothing:
    def __init__(self, name, imgURL, clothingID):
        self.objectName = name
        self.warmthRating = 0
        self.clothingID = clothingID
        self.classification = ""
        self.imgURL = imgURL

    # getters
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
    
    # setters
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



