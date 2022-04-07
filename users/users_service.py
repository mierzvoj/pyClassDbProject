import sqlite3

import meta as meta
import sqlalchemy
from sqlalchemy import create_engine, update, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from database import users_model
from database.database import SessionManager, engine
from database.users_model import User
import csv
import getpass
import bcrypt
import os



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
        self.room_id = None
        self.isroomcreated = None
        self.current_path = None
        self.hashed_room_id = None
        self.room_name = None

    current_path = os.getcwd()
    timings_csv_file = current_path + '\\rooms.csv'

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
        Session = sessionmaker(bind=UserManager.engine)
        session = Session()
        while not self.islogged:
            self.name = input('Podaj swój login: ')
            self.password = getpass.getpass("Podaj swoje hasło: ")
            self.bytespass = self.password.encode('utf-8')
            user = session.query(session.query(User).filter_by(name=self.name).exists()).scalar()
            user_passwd = session.query(User.password).filter(User.name == self.name).one_or_none()
            result = user_passwd[0]
            if user and bcrypt.checkpw(self.bytespass, result):
                print("Zalogowałeś się ")
                self.islogged = True
                break
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
        query = "SELECT name from users"
        my_cursor = engine.execute(query)
        for row in my_cursor:
            print("użytkownik systemu: " + row[0])

    def showAllUserRooms(self):
        Session = sessionmaker(bind=UserManager.engine)
        session = Session()
        rooms = session.query(User.room)
        result = rooms[0]
        print(result)

    def findUserByName(self):
        self.input_name = input('Podaj nazwę użytkownika do wyszukania: ')
        Session = sessionmaker(bind=UserManager.engine)
        session = Session()
        user = session.query(session.query(User).filter_by(name=self.input_name).exists()).scalar()
        q = session.query(User.name).filter(User.name == self.input_name).one_or_none()
        if user:
            result = q[0]
            print("Znaleziono rekord: " + result)
        else:
            print("Nie znaleziono takiego użytkownika")
        session.close()

    def deleteEntry(self):
        self.input_name = input('Podaj nazwę użytkownika do usuniecia: ')
        Session = sessionmaker(bind=UserManager.engine)
        session = Session()
        user = session.query(session.query(User).filter_by(name=self.input_name).exists()).scalar()
        q = session.query(User.name).filter(User.name == self.input_name).one_or_none()
        if user:
            session.query(User).filter(User.name == self.input_name).delete()
            session.commit()
            session.close()
            print("Rekord został usunięty")
        else:
            print("Nie znaleziono takiego użytkownika")

    def options(self):
        while self.islogged:
            print("Witamy w programie logowania\n")
            print("Wybierz opcję menu lista: 1/szukaj: 2/usun: 3/utwórz pokój: 4/pokaż pokoje: 5/dodaj usera do pokoju: 6/zakoncz: 7\n")
            menu = int(input("podaj wybór: "))
            if menu == 1:
                self.showAllUsers()
            elif menu == 2:
                self.findUserByName()
            elif menu == 3:
                self.deleteEntry()
            elif menu == 4:
                self.createNewRoom()
            elif menu == 5:
                self.showAllUserRooms()
            elif menu == 6:
                self.addUserToRoom()
            else:
                exit()

    def createNewRoom(self):
        self.islogged = True
        self.room_id = input("Id pokoju powinno mieć cztery cyfry: ")
        self.verifyRoomId(self.room_id)
        while True:
            room_password = getpass.getpass("Podaj hasło z cyfr o długości co najmniej 4 znaków: ")
            if len(room_password) >= 4 and room_password.isdigit():
                print("Poprawne hasło")
                break
            else:
                print("Hasło musi mieć co najmniej 4 cyfry")
        while True:
            self.room_name = input("Podaj nazwę pokoju: ")
            if len(self.room_name) > 0:
                print("Poprawna nazwa pokoju")
                break
            else:
                print("Podaj nazwę pokoju")
        with open(self.timings_csv_file, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            self.hashed_room_id = bcrypt.hashpw(room_password.encode('utf8'), bcrypt.gensalt())
            csv_writer.writerow([self.room_id, self.hashed_room_id, self.room_name, self.name])
            csvfile.close()
            print("Zarejestrowałeś nowy pokój")
            self.isroomcreated = True
        self.options()

    def verifyRoomId(self, room_id):
        csv_file = csv.reader(open(self.timings_csv_file, "r"))
        print(room_id)
        while True:
            for row in csv_file:
                if self.room_id == row[0]:
                    print("Pokój o takim id już istnieje")
                    print("Zarejestruj nowy pokój")
                    self.createNewRoom()
                break
            else:
                print("Id pokoju ok")
            break

    def addUserToRoom(self):
        meta = MetaData(bind=engine)
        MetaData.reflect(meta)
        usertobeadded = input("Podaj name usera do dodania: ")
        roomtobeused = input("Podaj id pokoju do dodania użytkownika: ")
        roompasswd = input("Podaj hasło do pokoju: ")
        Session = sessionmaker(bind=UserManager.engine)
        session = Session()
        user = session.query(session.query(User).filter_by(name=usertobeadded).exists()).scalar()
        q = session.query(User.name).filter(User.name == usertobeadded).one_or_none()
        if user:
            result = q[0]
            print(result)
            USERS = meta.tables['users']
            stmt = USERS.update().where(USERS.c.name == usertobeadded).values(room=roomtobeused)
            engine.execute(stmt)
            print("User dodany do pokoju")
        else:
            print("nie znaleziono pokoju lub użytkownika")