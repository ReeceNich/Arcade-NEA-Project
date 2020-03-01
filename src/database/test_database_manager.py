from database_manager import *
import unittest

d = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))


class TestAuthUser(unittest.TestCase):

    def test_auth_user_normal(self):
        self.assertEqual(d.auth_user('rnicholls13', '5678', 1), True, "Normal auth user correct failed")
    
    def test_auth_user_normal_incorrect(self):
        self.assertEqual(d.auth_user('rnicholls13', '0000', 1), False, "Normal auth user incorrect failed")



if __name__ == "__main__":
    # d = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))

    unittest.main()