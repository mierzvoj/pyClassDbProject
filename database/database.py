from sqlalchemy.orm import sessionmaker

from database import users_model



class Database():

    def insert(self):
        Session = sessionmaker(bind=users_model.engine)
        session = Session()

        us = users_model.User(1 , 'wojtek', 'login1234')
        session.add(us)

        session.commit()
