import sqlite3

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from database import users_model
from database.database import SessionManager, engine
from database.users_model import User
import csv
import getpass
import bcrypt


class UserManager(SessionManager):
    Base = declarative_base()
    engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)

    def __init__(self):
        self.name = None
        self.password = None
        self.islogged = False
        self.hashed = None
        self.path = None
        self.new_user = None
        self.bytespass = None
        self.user_passwd = None
        self.input_name = None

    def createNewUser(self):
        print("tu createNewUser")
        pattern = r'^[A-Z]{3}'
        print("Podaj login i hasło, aby się zarejestrować ")
        self.name = input(
            "Podaj login w register, login musi zaczynać się trzema wielkimi literami i mieć jedną cyfrę: ")
        self.verifyLogin(self.name)
        while True:
            self.password = getpass.getpass("Podaj hasło o długości co najmniej 6 znaków z jedną cyfrą: ")
            if len(self.password) >= 6 and any(char.isdigit() for char in self.password):
                print("Poprawne hasło")
                break
            else:
                print("hasło musi mieć co najmniej 6 znaków i jedną cyfrę")
        print("continue my code")
        self.hashed = bcrypt.hashpw(self.password.encode('utf8'), bcrypt.gensalt())
        new_user = User(self.name, self.hashed)
        print(repr(new_user))
        Session = sessionmaker(bind=UserManager.engine)
        session = Session()
        session.add(new_user)
        session.commit()
        print("Zarejestrowałeś się")
        self.islogged = True
        self.options()
        print("commit unsuccesfull")

    def login(self):
        while not self.islogged:
            self.name = input('Podaj swój login: ')
            self.password = getpass.getpass("Podaj swoje hasło: ")
            self.bytespass = b"self.password"
            self.hashed = bcrypt.hashpw(self.bytespass, bcrypt.gensalt())
            Session = sessionmaker(bind=UserManager.engine)
            session = Session()
            user = session.query(session.query(User).filter_by(name=self.name).exists()).scalar()
            user_passwd = session.query(User.password).filter(User.name == self.name).one_or_none()
            result = user_passwd[0]
            print(user)
            print(result)
            print(self.hashed)
            if user and bcrypt.hashpw(self.bytespass, result):
                print("Zalogowałeś się ")
                self.islogged = True
                # session['logged_in'] = True
            else:
                print('Nieprawidłowy login lub hasło')
                print('Spróbuj się zarejestrować')
                self.createNewUser()
        print("tu options")
        session.close()
        self.options()


    def verifyLogin(self, name):
        if not any(char.isdigit() for char in name):
            print('Podaj choć jedną cyfrę w loginie użytkownika')
            self.createNewUser()
        else:
            while True:
                Session = sessionmaker(bind=UserManager.engine)
                session = Session()
                user = session.query(session.query(User).filter_by(name=self.name).exists()).scalar()
                if user:
                        print("Użytkownik o takim loginie już istnieje")
                        print("Zarejestruj się jako nowy użytkownik o innym loginie")
                        self.createNewUser()
                break
        session.close()

    def showAllUsers(self):
        q = "SELECT name from users"
        my_cursor = engine.execute(q)
        for row in my_cursor:
            print("użytkownik systemu: " + row[0])


    def findUserByName(self):
        self.input_name = input('Podaj nazwę do wyszukania: ')
        q = 'SELECT * FROM users WHERE name=input_name'
        my_cursor = engine.execute(q)
        for row in my_cursor:
            print("użytkownik systemu: " + row[0])

    def deleteEntry(self):
        pass

    def options(self):
        while self.islogged:
            print("Witamy w programie logowania\n")
            print("Wybierz opcję menu lista: 1/szukaj: 2/usun: 3/zakoncz: 4\n")
            menu = int(input("podaj wybór: "))
            if menu == 1:
                self.showAllUsers()
            elif menu == 2:
                self.findUserByName()
            elif menu == 3:
                print("Wybrany użytkownik został usunięty z rejestru, tej operacji nie można odwrócić")
            else:
                exit()
