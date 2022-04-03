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

    name = Column(String, primary_key=True)
    password = Column(String)

    def __init__(self, name, password):
        self.name = name
        self.password = password


base.metadata.create_all(engine)
