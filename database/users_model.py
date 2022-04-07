from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base

from database.database import Base

load_dotenv()

from sqlalchemy import Column, String, Integer, create_engine



class User(Base):
    __tablename__ = 'users'

    name = Column(String, primary_key=True)
    password = Column(String)
    room = Column(String)

    def __init__(self, name, password, room):
        self.name = name
        self.password = password
        self.room = room

    def __repr__(self):
        return "<User(name='%s')>" % (
            self.name)
