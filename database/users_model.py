import sqlite3
from os import getenv
from sys import argv

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
base = declarative_base()


class User(base):
    __tablename__ = 'users'

    users_id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def __init__(self, users_id, name, password):
        self.users_id = users_id
        self.name = name
        self.password = password


base.metadata.create_all(engine)
