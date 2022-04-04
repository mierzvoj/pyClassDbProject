from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

Base = declarative_base()
engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)


class SessionManager(object):
    def __init__(self):
        self.session = Session()


