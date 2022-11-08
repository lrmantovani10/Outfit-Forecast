import unittest
from backend_functions import *


# Tries to connect and insert to a mongodb database based on
# Testing the connection to the database
def connection_link_tester(link):
    client = pymongo.MongoClient(link)
    try:
        db = client["Clothing"]
        collection = db["Test"]
        test = {"unittest": "ok"}
        collection.insert_one(test)
        return True
    except:
        return False


class TestConnection(unittest.TestCase):

    # Initially ran into SSL certificate issues for realLink below
    # To fix install these certificates that MongoDB uses (https://stackoverflow.com/a/69407602), as the default Windows ones are expired in terms of what MongoDB requires
    # If this test fails that is why ^
    def test_connection(self):
        realLink = "mongodb://DGilb23:Bhhe2nsBOXwI4Axh@ac-m14bdu9-shard-00-00.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-01.mpb6ff1.mongodb.net:27017,ac-m14bdu9-shard-00-02.mpb6ff1.mongodb.net:27017/?ssl=true&replicaSet=atlas-pfj1lz-shard-0&authSource=admin&retryWrites=true&w=majority"
        fakeLink = "yo yo yo"
        self.assertFalse(connection_link_tester(fakeLink))

        # This will have added a valid entry to the db
        self.assertTrue(connection_link_tester(realLink))

        client = pymongo.MongoClient(realLink)
        db = client["Clothing"]
        collection = db["Test"]

        # This document can only be made by connection_link_tester above, so it should exist
        self.assertTrue(collection.count_documents({"unittest": "ok"}) > 0)

        # This fake document should not exist
        self.assertFalse(collection.count_documents({'doesNotExist': 'Fake'}) > 0)


class TestUser(unittest.TestCase):

    def test_username(self):
        newUser = User("a", [], [], [], [])
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
        newUser = User("a", [], [], [], [])
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
        newUser = User("a", [], [], [], [])
        self.assertEqual(newUser.getWardrobe(), [])
        test_img = "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7"
        newClothing = Clothing("t-shirt", "topInner", test_img, 0)
        self.assertTrue(newUser.updateWardrobe(newClothing))
        self.assertFalse(newUser.updateWardrobe("t-shirt"), "must update wardobe with clothing item")
        self.assertEqual(newUser.getWardrobe(), [newClothing])

    def test_currOutfit(self):
        newUser = User("a", [], [], [], [])
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
        newUser = User("a", [], [], [], [])
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

    # test that classifyNew correctly adds a clothing item to user's wardrobe
    # in reality, when user takes photo, ImageData class will call upload_image on that image which sends
    # it to the bucket, then gets the firebase URL and calls classifyNew with that URL
    def test_classifyNew(self):
        newUser = User("a", [], [], [], [])
        self.assertEqual(newUser.getWardrobe(), [])
        # google vision api takes imageURL from firebase
        testImg = "gs://first-bucket-example/jeans.jpeg"
        newUser.classifyNew(testImg)
        testItem = Clothing("jeans", "bottom", testImg, 0)
        updatedWardrobe = newUser.getWardrobe()
        self.assertEqual(updatedWardrobe, [testItem])
        testImg2 = "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-sweater"  # faulty URL, which doesn't work
        self.assertFalse(newUser.classifyNew(testImg2))
        self.assertEqual(newUser.getWardrobe(), [testItem])


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

    def test_warmthRating(self):
        newClothing = Clothing("t-shirt", "topInner",
                               "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7",
                               0)
        self.assertEqual(newClothing.getWarmthRating(), 0)
        self.assertTrue(newClothing.setWarmthRating(0))
        self.assertFalse(newClothing.setWarmthRating("0"), "warmthRating must be type int")

    def test_classification(self):
        newClothing = Clothing("t-shirt", "topInner",
                               "https://firebasestorage.googleapis.com/v0/b/outfit-forecast.appspot.com/o/test-shirt.jpg?alt=media&token=a4a90723-2a59-4ed0-aa4e-e44a7aba57b7",
                               0)
        self.assertTrue(newClothing.setClassification("bottom"))
        self.assertFalse(newClothing.setClassification("warm top"), "classification is not top/bottom/shoes")
        self.assertTrue(newClothing.setClassification("top"))
        self.assertEqual(newClothing.getClassification(), "top")

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