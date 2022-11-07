import pymongo
import re

class User:
    def __init__(self, username):
        if not self.setUsername(username):
            self.username = ""
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

    # must be of type _
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
    
    '''
    call google vision api on imgURL to get back classification
    parse classification (maybe preset categories and if it falls in one of those you take it)
    create clothing item
    call updateWardrobe on that clothing item
    '''
    def classifyNew(self, imgURL):
        return True



class Clothing:
    def __init__(self, name, classification, imgURL, clothingID):
        # Trust constructor usage for now (depends on how front-end uses this)
        self.objectName = name
        self.classification = classification
        self.clothingID = clothingID
        self.imgURL = imgURL

    # ------- getters -------
    def getObjectName(self):
        return self.objectName

    def getClothingID(self):
        return self.clothingID
    
    def getClassification(self):
        return self.classification

    def getImgURL(self):
        return self.imgURL
    
    # ------- setters -------
    def setObjectName(self, name):
        if isinstance(name, str) and name != "" and any(c.isalpha() for c in name):
            self.objectName = name
            return True
        return False

    def setClassification(self, name):
        if name == "top" or name == "bottom" or name == "shoes":
            self.classification = name
            return True
        return False