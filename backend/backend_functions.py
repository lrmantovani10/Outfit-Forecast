class User:
  def __init__(self, username):
    self.username = username
    self.wardrobe = []
    self.clothingHistory = []
    self.preferences = []

  def getUsername(self):
      return self.username

  def setUsername(self):
      return True   

  def getWardrobe(self):
      return self.wardrobe

  def updateWardrobe(self):
      return True

  def setPreference(self):
      return True

  def getPreferences(self):
      return []  
  
  def setLocation(self):
      return True   
  
  def getLocation(self):
      return []            
  
  def setCurrOutfit(self):
      return True   
  
  def getCurrOutfit(self):
      return []           
  
  def updateClothingHistory(self):
      return True   
  
  def getClothingHistory(self):
      return []           

  def classifyNew(self):
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
  def setObjectName(self):
      return True

  def setWarmthRating(self):
      return True
  
  def setClassification(self):
      return True

class enviornmentalData:
  def __init__(self):
    newUser = User("")
    self.enviroData = newUser
    
  def getWeather():
    return []



