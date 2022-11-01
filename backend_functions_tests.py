import unittest
from backend_functions import *

class TestUser(unittest.TestCase):

    def test_username(self):
        newUser = User(" ")
        self.assertFalse(newUser.set_username("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklm"), "Username is more than 32 characters") 
        self.assertFalse(newUser(""), "Username is empty") 
        self.assertFalse(newUser.set_username("123456"), "Username must have at least one letter") 
        self.assertFalse(newUser.set_username("abcd"), "Username must have at least 1 number") 
        self.assertTrue(newUser.set_username("abcde12"))
        self.assertEqual(newUser.get_username(), "abcde12")
        self.assertFalse(newUser.set_username("0123abcdefg"), "Username cannot start with a number") 
        self.assertEqual(newUser.get_username(), "abcde12")
        self.assertFalse(newUser.set_username("abcdefg123!!"), "Username cannot have special characters") 

    def test_preferences(self):
        newUser = User(" ")
        self.assertFalse(newUser.set_preference([-20, 70], "Temperature cannot be below -20 Farenheit")) 
        self.assertFalse(newUser.set_preference([0, 130], "Temperature cannot be above 120 Farenheit"))
        self.assertTrue(newUser.set_preference([-10, 120])) # Lower and upper bound included
        self.assertEqual(newUser.get_preferences(), [[-10, 120]])
        self.assertTrue(newUser.set_preference([0, 65]))
        self.assertEqual(newUser.get_preferences(), [[-10, 120], [0, 65]])
        self.assertFalse(newUser.set_preference([130], "Preference must be an array of 2 elements"))
        self.assertFalse(newUser.set_preference([], "Preference must be an array of 2 elements"))

    # Location API returns latitude, longitude pair
    def test_location(self):
        newUser = User(" ")
        self.assertFalse(newUser.set_location([-95, 70], "Latitude must be between -90 and 90 degrees")) 
        self.assertFalse(newUser.set_location([95, 70], "Latitude must be between -90 and 90 degrees")) 
        self.assertFalse(newUser.set_location([50, -182], "Longitude must be between -180 and 180 degrees")) 
        self.assertFalse(newUser.set_location([50, 182], "Longitude must be between -180 and 180 degrees")) 
        self.assertFalse(newUser.set_location([-182], "Location must have 2 values"))
        self.assertFalse(newUser.set_location([], "Location must have 2 values")) 
        self.assertTrue(newUser.set_location([50, 65]))
        self.assertEqual(newUser.get_location(), [50, 65])
    
    # no set_wardrobe because classifyNew() will handle appending items to wardrobe
    def test_wardrobe(self):
        newUser = User(" ")
        self.assertEqual(newUser.get_wardrobe(), [])

    # test that classifyNew correctly adds a clothing item to user's wardrobe
    def test_classifyNew(self):
        newUser = User(" ")
        self.assertEqual(newUser.get_wardrobe(), [])
        test_img = "gs://first-bucket-example/t-shirt.jpg" # google vision api takes imageURI from cloud storage bucket
        newUser.classifyNew(test_img)
        test_item = Clothing("t-shirt", test_img, 0)
        updated_wardrobe = newUser.get_wardrobe()
        self.assertEqual(updated_wardrobe, [test_item])

class TestClothing(unittest.TestCase):

    def test_objectName(self):
        newClothing = Clothing("t-shirt", "gs://first-bucket-example/t-shirt.jpg", 0)
        self.assertEqual(newClothing.get_objectName(), "t-shirt")
        self.assertTrue(newClothing.set_objectName("t-shirt"))
        self.assertFalse(newClothing.set_objectName(""), "objectName is empty") 
        self.assertFalse(newClothing.set_objectName("123456"), "objectName must have at least one letter")
        self.assertFalse(newClothing.set_objectName(0), "objectName must be type string") 

    def test_warmthRating(self):
        newClothing = Clothing("t-shirt", "gs://first-bucket-example/t-shirt.jpg", 0)
        self.assertEqual(newClothing.get_warmthRating(), 0)
        self.assertTrue(newClothing.set_warmthRating(0))
        self.assertFalse(newClothing.set_warmthRating("0"), "warmthRating must be type int")

    def test_classification(self):
        newClothing = Clothing("t-shirt", "gs://first-bucket-example/t-shirt.jpg", 0)
        self.assertTrue(newClothing.set_classification("top"))
        self.assertFalse(newClothing.set_classification(""), "classification cannot be empty")
        self.assertFalse(newClothing.set_classification(0), "classification must be type string")
        self.assertFalse(newClothing.set_classification("1"), "classification cannot have numbers")
        self.assertFalse(newClothing.set_classification("top!"), "classification cannot have special characters")
        newClothing.set_classification("top")
        self.assertEqual(newClothing.get_classification(), "top")

if __name__ == '__main__':
        unittest.main() 