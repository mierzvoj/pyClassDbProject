from os import getenv

from sqlalchemy.orm import sessionmaker

from database import users_model
from database.users_model import User
from users.users_service import LoggingApi
from database.database import Database
import sqlite3
from sqlite3 import Error


def run():
    if __name__ == '__main__': run()


def begin():
    newapi = createNewLoggingApi()

    print("Witaj")
    while True:
        try:
            option = int(input("Zaloguj albo zarejestruj się: 1 lub 2 "))
            if option in ['1', '2']:
                break
            if option == 1:
                newapi.login()
            else:
                newapi.register()
            newapi.options()
        except:
            print("Zacznij od nowa")
            break


def createNewLoggingApi():
    newapi = LoggingApi()
    return newapi


def createNewDatabase():
    newdatabase = User(getenv('DB_NAME'))
    return newdatabase


print(getenv("DB_NAME"))

insert1 = Database()
insert1.insert()

Session = sessionmaker(bind=users_model.engine)
session = Session()

us = users_model.User(1, 'wojtek3', 'login1234')
session.add(us)

session.commit()



u = User('1000', 'wojtek2', 'blabla')
insert1.add(u)

begin()
