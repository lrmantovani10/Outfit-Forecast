class User:
  def __init__(self, username):
    self.username = username
    self.wardrobe = []
    self.clothingHistory = []
    self.preferences = []

  def get_username(self):
      return self.username

class Clothing:
  def __init__(self, name, imgURL, clothingID):
    self.objectName = name
    self.warmthRating = 0
    self.clothingID = clothingID
    self.classification = ""
    self.imgURL = imgURL

  # getters
  def get_objectName(self):
    return self.objectName

  def get_warmthRating(self):
      return self.warmthRating

  def get_clothingID(self):
      return self.clothingID
  
  def get_classification(self):
      return self.classification

  def get_imgURL(self):
      return self.imgURL
  
  # setters
  def set_objectName(self):
      return True

  def set_warmthRating(self):
      return True
  
  def set_classification(self):
      return True

class enviornmentalData:
  def __init__(self, username):


