from users.users_service import LoggingApi
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


import os

print(os.getcwd())

begin()
