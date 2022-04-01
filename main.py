from LoggingApiModule import LoggingApi
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

def create_connection():

    conn = None;
    try:
        conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

create_connection()
begin()
