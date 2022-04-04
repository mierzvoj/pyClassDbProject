from os import getenv
from database.users_model import User

from sqlalchemy.orm import sessionmaker

from database import users_model

from database.users_model import User
from users.users_service import UserManager
import sqlite3
from sqlite3 import Error


def run():
    if __name__ == '__main__': run()



def begin():
    new_session = createNewUserService()

    print("Witaj")
    while True:
        try:
            option = int(input("Zaloguj albo zarejestruj się: 1 lub 2 "))
            if option in ['1', '2']:
                break
            if option == 1:
                new_session.login()
            else:
                new_session.createNewUser()
            new_session.options()
        except:
            print("Zacznij od nowa")
            break


def createNewUserService():
    user_manager = UserManager()
    return user_manager


def createNewDatabase():
    newdatabase = User(getenv('DB_NAME'))
    return newdatabase


print(getenv("DB_NAME"))




begin()
