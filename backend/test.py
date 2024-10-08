# backend/test.py

import os
import unittest
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv('config/.env')


class DatabaseConnectionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the database connection before running tests."""
        cls.db_name = os.getenv("DB_NAME")  # Change this to your actual variable name
        cls.db_user = os.getenv("DB_USER")  # Change this to your actual variable name
        cls.db_password = os.getenv("DB_PASSWORD")  # Change this to your actual variable name
        cls.db_host = os.getenv("DB_HOST")  # Change this to your actual variable name
        cls.db_port = os.getenv("DB_PORT")  # Change this to your actual variable name

        # Establish a connection to the PostgreSQL database
        cls.connection = psycopg2.connect(
            dbname=cls.db_name,
            user=cls.db_user,
            password=cls.db_password,
            host=cls.db_host,
            port=cls.db_port
        )

    def test_connection(self):
        """Test if the database connection is successful."""
        self.assertIsNotNone(self.connection)
        self.assertEqual(self.connection.closed, 0)  # 0 means the connection is open

    @classmethod
    def tearDownClass(cls):
        """Close the database connection after tests."""
        cls.connection.close()


if __name__ == '__main__':
    unittest.main()
