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


if __name__ == '__main__':
        unittest.main() 