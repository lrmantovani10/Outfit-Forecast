import unittest
import backend_functions

class TestUser(unittest.TestCase):
    # currentUser = User("asdasda88>>?")

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


if __name__ == '__main__':
        unittest.main() 