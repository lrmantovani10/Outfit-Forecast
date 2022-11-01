import unittest
from backend_functions import *

class TestUser(unittest.TestCase):
    newUser = User(" ")

    def test_username(self):
        self.assertFalse(self.set_username("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklm"), "Username is more than 32 characters") 
        self.assertFalse(self.set_username(""), "Username is empty") 
        self.assertFalse(self.set_username("123456"), "Username must have at least one letter") 
        self.assertFalse(self.set_username("abcd"), "Username must have at least 1 number") 
        self.assertTrue(self.set_username("abcde12"))
        self.assertEqual(self.get_username(), "abcde12")
        self.assertFalse(self.set_username("0123abcdefg"), "Username cannot start with a number") 
        self.assertEqual(self.get_username(), "abcde12")
        self.assertFalse(self.set_username("abcdefg123!!"), "Username cannot have special characters") 

    def test_preferences(self):
        self.assertFalse(self.set_preference([-20, 70], "Temperature cannot be below -20 Farenheit")) 
        self.assertFalse(self.set_preference([0, 130], "Temperature cannot be above 120 Farenheit"))
        self.assertTrue(self.set_preference([-10, 120])) # Lower and upper bound included
        self.assertEqual(self.get_preferences(), [[-10, 120]])
        self.assertTrue(self.set_preference([0, 65]))
        self.assertEqual(self.get_preferences(), [[-10, 120], [0, 65]])
        self.assertFalse(self.set_preference([130], "Preference must be an array of 2 elements"))
        self.assertFalse(self.set_preference([], "Preference must be an array of 2 elements"))
        

if __name__ == '__main__':
        unittest.main() 