from sqlalchemy.orm import sessionmaker

from database import users_model


class Database:

    def insert(self, user):
        Session = sessionmaker(bind=users_model.engine)
        session = Session()

        us = users_model.User(user)

        session.add(us)

        session.commit()
