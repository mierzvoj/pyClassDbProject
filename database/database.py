import sqlite3
from os import getenv
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor =self.connection.cursor()

    def __del__(self):
        self.connection.close()