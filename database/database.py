from sqlalchemy.orm import sessionmaker

from database import users_model



class Database():

    def insert(self):
        Session = sessionmaker(bind=users_model.engine)
        session = Session()

<<<<<<< HEAD
        us = users_model.User(999, 'wojtek1', 'login1234')
=======
        us = users_model.User(1 , 'wojtek', 'login1234')
>>>>>>> 57b3294c581940392bf289083539175930e2fbcb
        session.add(us)

        session.commit()
