import unittest
import requests
from backend_functions import *
from urllib.parse import quote_plus
from datetime import datetime


# Tries to connect and insert to a mongodb database based on
# Testing the connection to the database
def connection_link_tester(link):
    client = pymongo.MongoClient(link)
    try:
        db = client["UnitTests"]
        collection = db["Test"]
        test = {"unittest": "ok"}
        collection.insert_one(test)
        return True
    except:
        return False

def clothingItemEquals(obj1, obj2):
    if obj1.getObjectName() == obj2.getObjectName() \
    and obj1.getClassification() == obj2.getClassification() \
    and obj1.getImgURL() == obj2.getImgURL() \
    and obj1.getClothingID() == obj2.getClothingID() \
    and obj1.getLowerBound() == obj2.getLowerBound() \
    and obj1.getUpperBound() == obj2.getUpperBound():
        return True
    else:
        return False

class TestConnection(unittest.TestCase):

    # Initially ran into SSL certificate issues for realLink below
    # To fix install these certificates that MongoDB uses (https://stackoverflow.com/a/69407602), as the default Windows ones are expired in terms of what MongoDB requires
    # If this test fails that is why ^
    def test_connection(self):
        realMongoLink = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"
        fakeLink = "yo yo yo"

        client = pymongo.MongoClient(realMongoLink)
        db = client["UnitTests"]
        collection = db["Test"]

        currCount = collection.count_documents({"unittest": "ok"})

        self.assertFalse(connection_link_tester(fakeLink))

        # This will have added a valid entry to the db
        self.assertTrue(connection_link_tester(realMongoLink))


        # Tester should have added a document
        self.assertTrue(collection.count_documents({"unittest": "ok"}) == currCount + 1)

        # This fake document should not exist
        self.assertFalse(collection.count_documents({'doesNotExist': 'Fake'}) > 0)

class TestFlask(unittest.TestCase):

    def test_recommender_endpoint(self):
        recommenderNewTest = requests.get('https://outfit-forecast.herokuapp.com/dailyRecommender/forunittests/60/65/63/nothing/new').json()
        recommenderNewExpected = [{'objectName': 'sweater', 'classification': 'topOuter', 'clothingID': 'leo-0',
                                   'imgURL': 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-sweater.jpg?alt=media&token=ded9d625-062e-4e61-bbdc-a3988104fb8b',
                                   'lowerTempBound': -10, 'upperTempBound': 110},
                                  {'objectName': 't-shirt', 'classification': 'topInner', 'clothingID': 'leo-1',
                                   'imgURL': 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7',
                                   'lowerTempBound': -20, 'upperTempBound': 120},
                                  {'objectName': 'sweatpants', 'classification': 'bottom', 'clothingID': 'leo-2',
                                   'imgURL': 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-sweatpants.jpg?alt=media&token=9c54025f-94f1-4759-9894-6df682867241',
                                   'lowerTempBound': -20, 'upperTempBound': 120},
                                  {'objectName': 'shoes', 'classification': 'shoes', 'clothingID': 'leo-3',
                                   'imgURL': 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shoes.jpg?alt=media&token=a1f187f2-ca97-41b2-a39f-8291f34849bd',
                                   'lowerTempBound': -20, 'upperTempBound': 120}]
        self.assertEqual(recommenderNewTest, recommenderNewExpected)

        recommenderRejectTest = requests.get('https://outfit-forecast.herokuapp.com/dailyRecommender/forunittests/60/65/63/nothing/reject').json()
        recommenderRejectExpected = [{'objectName': 'hoodie', 'classification': 'topOuter', 'clothingID': 'leo-4',
                                   'imgURL': 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-hoodie.jpg?alt=media&token=b761f8de-6679-42d4-a68d-f434e748dfb7',
                                   'lowerTempBound': -20, 'upperTempBound': 120},
                                  {'objectName': 't-shirt', 'classification': 'topInner', 'clothingID': 'leo-1',
                                   'imgURL': 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7',
                                   'lowerTempBound': -20, 'upperTempBound': 120},
                                  {'objectName': 'sweatpants', 'classification': 'bottom', 'clothingID': 'leo-2',
                                   'imgURL': 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-sweatpants.jpg?alt=media&token=9c54025f-94f1-4759-9894-6df682867241',
                                   'lowerTempBound': -20, 'upperTempBound': 120},
                                  {'objectName': 'shoes', 'classification': 'shoes', 'clothingID': 'leo-3',
                                   'imgURL': 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shoes.jpg?alt=media&token=a1f187f2-ca97-41b2-a39f-8291f34849bd',
                                   'lowerTempBound': -20, 'upperTempBound': 120}]
        self.assertEqual(recommenderRejectTest, recommenderRejectExpected)

    def test_classification_endpoint(self):
        realMongoLink = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"
        client = pymongo.MongoClient(realMongoLink)
        db = client["User"]
        userCollection = db["Test"]

        match = userCollection.find({'username': 'forclothingaddition'})[0]
        wardrobeLength = len(match['wardrobe'])
        url = 'https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-hoodie.jpg?alt=media&token=b761f8de-6679-42d4-a68d-f434e748dfb7'
        quoted = quote_plus(url)
        requests.get('https://outfit-forecast.herokuapp.com/classifyNew/forclothingaddition/' + quoted + '/60/65')

        match = userCollection.find({'username': 'forclothingaddition'})[0]
        wardrobeLength2 = len(match['wardrobe'])

        self.assertEqual(wardrobeLength + 1, wardrobeLength2)

    def test_user_creation_endpoint(self):
        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y, %H:%M:%S").replace(", ", "-").replace("/", "-").replace(":", "-")
        username = "testuser-" + timestamp
        requests.get('https://outfit-forecast.herokuapp.com/createUser/' + username)

        realMongoLink = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"
        client = pymongo.MongoClient(realMongoLink)
        db = client["User"]
        userCollection = db["Test"]

        try:
            match = userCollection.find({'username': username})
            self.assertEqual(True, True)
        except:
            self.assertEqual(False, True)


class TestUser(unittest.TestCase):

    def test_username(self):
        newUser = User("a", [], [], [], [], [])
        self.assertFalse(newUser.setUsername("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklm"),
                         "Username is more than 32 characters")
        self.assertFalse(newUser.setUsername(""), "Username is empty")
        self.assertFalse(newUser.setUsername("123456"), "Username must have at least one letter")
        self.assertTrue(newUser.setUsername("abcd"))
        self.assertTrue(newUser.setUsername("abcde12"))
        self.assertEqual(newUser.getUsername(), "abcde12")
        self.assertFalse(newUser.setUsername("a "), "Username cannot have whitespace")
        self.assertFalse(newUser.setUsername("0123abcdefg"), "Username cannot start with a number")
        self.assertFalse(newUser.setUsername("abcdefg123!!"), "Username cannot have special characters")

    # Location API returns latitude, longitude pair
    def test_location(self):
        newUser = User("a", [], [], [], [], [])
        self.assertFalse(newUser.setLocation([-95, 70]), "Latitude must be between -90 and 90 degrees")
        self.assertFalse(newUser.setLocation([95, 70]), "Latitude must be between -90 and 90 degrees")
        self.assertFalse(newUser.setLocation([50, -182]), "Longitude must be between -180 and 180 degrees")
        self.assertFalse(newUser.setLocation([50, 182]), "Longitude must be between -180 and 180 degrees")
        self.assertFalse(newUser.setLocation([-182]), "Location must have 2 values")
        self.assertFalse(newUser.setLocation([]), "Location must have 2 values")
        self.assertTrue(newUser.setLocation([50, 65]))
        self.assertTrue(newUser.getLocation(), [50, 65])

    # no set_wardrobe because classifyNew() will handle appending items to wardrobe
    def test_wardrobe(self):
        newUser = User("a", [], [], [], [], [])
        self.assertEqual(newUser.getWardrobe(), [])
        test_img = "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7"
        newClothing = Clothing("t-shirt", "topInner", test_img, 0)
        self.assertTrue(newUser.updateWardrobe(newClothing))
        self.assertFalse(newUser.updateWardrobe("t-shirt"), "must update wardobe with clothing item")
        self.assertEqual(newUser.getWardrobe(), [newClothing])

    def test_currOutfit(self):
        newUser = User("a", [], [], [], [], [])
        fit1 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2), Clothing("Sandals", "shoes", "URL", 3)]
        fit2 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2)]
        fit3 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2), Clothing("Sandals", "shoes", "URL", 3),
                Clothing("Sneakers", "shoes", "URL", 4)]
        self.assertTrue(newUser.setCurrOutfit(fit1))
        self.assertEqual(newUser.getCurrOutfit(), fit1)
        self.assertFalse(newUser.setCurrOutfit(fit2), "There must be 4 clothing objects")
        self.assertFalse(newUser.setCurrOutfit(fit3), "There must be 4 clothing objects")
        self.assertFalse(newUser.setCurrOutfit(["jacket", "shirt", "jeans", "shoes"]), "These are not clothing objects")

    def test_clothingHistory(self):
        newUser = User("a", [], [], [], [], [])
        fit1 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2), Clothing("Sandals", "shoes", "URL", 3)]
        fit2 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2)]
        fit3 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2), Clothing("Sandals", "shoes", "URL", 3),
                Clothing("Sneakers", "shoes", "URL", 4)]
        fit4 = [Clothing("Sweater", "topOuter", "URL", 0), Clothing("Dress Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2), Clothing("Sandals", "shoes", "URL", 3)]
        self.assertTrue(newUser.updateClothingHistory(fit1))
        self.assertEqual(newUser.getClothingHistory(), [fit1])
        self.assertFalse(newUser.updateClothingHistory(fit2), "There must be 4 clothing objects in the fit")
        self.assertEqual(newUser.getClothingHistory(), [fit1])
        self.assertFalse(newUser.updateClothingHistory(fit3), "There must be 4 clothing objects in the fit")
        self.assertEqual(newUser.getClothingHistory(), [fit1])
        self.assertTrue(newUser.updateClothingHistory(fit4))
        self.assertEqual(newUser.getClothingHistory(), [fit1, fit4])

    def test_rejected(self):
        newUser = User("a", [], [], [], [], [])
        fit1 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2), Clothing("Sandals", "shoes", "URL", 3)]
        fit2 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2)]
        fit3 = [Clothing("Jacket", "topOuter", "URL", 0), Clothing("T-Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2), Clothing("Sandals", "shoes", "URL", 3),
                Clothing("Sneakers", "shoes", "URL", 4)]
        fit4 = [Clothing("Sweater", "topOuter", "URL", 0), Clothing("Dress Shirt", "topInner", "URL", 1),
                Clothing("Jeans", "bottom", "URL", 2), Clothing("Sandals", "shoes", "URL", 3)]
        self.assertTrue(newUser.updateRejected(fit1))
        self.assertEqual(newUser.getRejected(), [fit1])
        self.assertFalse(newUser.updateRejected(fit2), "There must be 4 clothing objects in the fit")
        self.assertEqual(newUser.getRejected(), [fit1])
        self.assertFalse(newUser.updateRejected(fit3), "There must be 4 clothing objects in the fit")
        self.assertEqual(newUser.getRejected(), [fit1])
        self.assertTrue(newUser.updateRejected(fit4))
        self.assertEqual(newUser.getRejected(), [fit1, fit4])
        
    # test that classifyNew correctly adds a clothing item to user's wardrobe
    # in reality, when user takes photo, ImageData class will call upload_image on that image which sends
    # it to the bucket, then gets the firebase URL and calls classifyNew with that URL
    def test_classifyNew(self):
        newUser = User("a", [], [], [], [], [])
        self.assertEqual(newUser.getWardrobe(), [])
        # google vision api takes imageURL from firebase
        testImg = "gs://first-bucket-example/shoes.jpg"
        testItem = Clothing("footwear", "shoes", testImg, "a-0", -20, 120)
        self.assertEqual(newUser.classifyNew(testImg, -20, 120), "Image Classified: footwear")
        updatedWardrobe = newUser.getWardrobe()
        # print(updatedWardrobe.__dict__)
        self.assertTrue(clothingItemEquals(updatedWardrobe[0], testItem))
        testImg2 = "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-sweater"  # faulty URL, which doesn't work
        self.assertEqual(newUser.classifyNew(testImg2, -20, 120), "API Error")
        self.assertTrue(clothingItemEquals(updatedWardrobe[0], testItem))
        testImg3 = "gs://first-bucket-example/t-shirt.jpg"
        testItem3 = Clothing("top", "topInner", testImg3, "a-1", -20, 120)
        self.assertEqual(newUser.classifyNew(testImg3, -20, 120), "Image Classified: top")
        self.assertTrue(clothingItemEquals(newUser.getWardrobe()[1], testItem3))
        testImg4 = "gs://first-bucket-example/pants.jpg"
        testItem4 = Clothing("shorts", "bottom", testImg4, "a-2", -20, 120)
        self.assertEqual(newUser.classifyNew(testImg4, -20, 120), "Image Classified: shorts")
        self.assertTrue(clothingItemEquals(newUser.getWardrobe()[2], testItem4))

    def test_dailyRecommender(self):
        newUser = User("a", [], [], [], [], [])
        testImg1 = "gs://first-bucket-example/shoes.jpg"
        testImg2 = "gs://first-bucket-example/jeans.jpeg"
        testImg3 = "gs://first-bucket-example/t-shirt.jpg"
        testImg4 = "gs://first-bucket-example/flannel.png"
        testItem1 = Clothing("sneakers", "shoes", testImg1, "a-0", -20, 120)
        testItem2 = Clothing("jeans", "bottom", testImg2, "a-1", -20, 120)
        testItem3 = Clothing("t-shirt", "topInner", testImg3, "a-2", -20, 120)
        testItem4 = Clothing("outerwear", "topOuter", testImg4, "a-3", -20, 120)
        testOutfit = [testItem4, testItem3, testItem2, testItem1]
        
        self.assertNotEqual(newUser.dailyRecommender([30, 40, 35, 'rain'], "new"), testOutfit, "There are no clothes in the wardrobe")
        self.assertEqual(newUser.dailyRecommender([30, 40, 35, 'rain'], "new"), None)

        newUser.updateWardrobe(testItem1)
        newUser.updateWardrobe(testItem2)
        newUser.updateWardrobe(testItem3)
        newUser.updateWardrobe(testItem4)

        outfit = newUser.dailyRecommender([30, 40, 35, 'rain'], "new")
        self.assertEqual(newUser.getRejected(), [])
        self.assertEqual(outfit, testOutfit)
        self.assertEqual(newUser.getClothingHistory(), [testOutfit])
        self.assertEqual(newUser.getCurrOutfit(), testOutfit)

        testImg5 = "gs://first-bucket-example/IMG_0077.jpg"
        testItem5 = Clothing("sweatshirt", "topOuter", testImg5, "a-4", -20, 120)
        newUser.updateWardrobe(testItem5)
        testOutfit2 = [testItem5, testItem3, testItem2, testItem1]
        outfit2 = newUser.dailyRecommender([30, 40, 35, 'rain'], "reject")
        self.assertEqual(newUser.getRejected(), [outfit]) # previous recommended outfit stored in currOutfit is rejected
        self.assertNotEqual(outfit2, testOutfit, "Rejected Outfits cannot be recommended again")
        self.assertEqual(outfit2, testOutfit2)
        self.assertEqual(newUser.getClothingHistory(), [outfit2]) # testOutfit gets removed from clothingHistory, as it is rejected
        self.assertEqual(newUser.getCurrOutfit, outfit2) # testOutfit gets removed from CurrOutfit, as it is rejected and replaced by outfit2

        outfit3 = newUser.dailyRecommender([30, 40, 35, 'rain'], "new")
        self.assertEqual(newUser.getRejected(), []) # Rejected list should be wiped
        self.assertEqual(outfit3, testOutfit) # testOutfit can be recommended again, because it has been removed from rejected
        self.assertEqual(newUser.getClothingHistory(), [outfit2, outfit3])
        self.assertEqual(newUser.getCurrOutfit, outfit3)

class TestClothing(unittest.TestCase):

    def test_objectName(self):
        newClothing = Clothing("t-shirt", "topInner",
                               "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7",
                               0)
        self.assertEqual(newClothing.getObjectName(), "t-shirt")
        self.assertTrue(newClothing.setObjectName("t-shirt"))
        self.assertFalse(newClothing.setObjectName(""), "objectName is empty")
        self.assertFalse(newClothing.setObjectName("123456"), "objectName must have at least one letter")
        self.assertFalse(newClothing.setObjectName(0), "objectName must be type string")

    def test_classification(self):
        newClothing = Clothing("t-shirt", "topInner",
                               "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7",
                               0)
        self.assertTrue(newClothing.setClassification("bottom"))
        self.assertFalse(newClothing.setClassification("warm top"), "classification is not top/bottom/shoes")
        self.assertTrue(newClothing.setClassification("topInner"))
        self.assertEqual(newClothing.getClassification(), "topInner")

    def test_bounds(self):
        newClothing = Clothing("t-shirt", "topInner",
                               "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7",
                               0)
        self.assertTrue(newClothing.setBounds(-20, 70))
        self.assertFalse(newClothing.setBounds(-20), "Need lower and upper bound argument")
        self.assertFalse(newClothing.setBounds(0, 130), "Temperature cannot be above 120 Farenheit")
        self.assertFalse(newClothing.setBounds(-21, 100), "Temperature cannot be below -20 Farenheit")

if __name__ == '__main__':
    unittest.main()