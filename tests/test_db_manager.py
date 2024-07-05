import unittest
from database.db_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(db_name=":memory:")

    def test_add_user(self):
        self.db.add_user("test_user")
        self.db.cursor.execute("SELECT * FROM users WHERE username = ?", ("test_user",))
        user = self.db.cursor.fetchone()
        self.assertIsNotNone(user)

    def tearDown(self):
        self.db.close()

if __name__ == '__main__':
    unittest.main()
