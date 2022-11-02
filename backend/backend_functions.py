import pymongo

class User:
  def __init__(self, username):
    self.username = username
    self.wardrobe = []
    self.clothingHistory = []
    self.preferences = []

  def getUsername(self):
      return self.username

  def setUsername(self, username):
      return True   

  def getWardrobe(self):
      return self.wardrobe

  def updateWardrobe(self, clothingItem):
      return True

  def setPreference(self, prefArr):
      return True

  def getPreferences(self):
      return []  
  
  def setLocation(self, locArr):
      return True   
  
  def getLocation(self):
      return []            
  
  def setCurrOutfit(self, fit):
      return True   
  
  def getCurrOutfit(self):
      return []           
  
  def updateClothingHistory(self, fit):
      return True   
  
  def getClothingHistory(self):
      return []           

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

class enviornmentalData:
  def __init__(self):
    newUser = User("")
    self.enviroData = newUser
    
  def getWeather():
    return []



