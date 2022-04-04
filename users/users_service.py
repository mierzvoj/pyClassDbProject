from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from database import users_model
from database.database import SessionManager
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
        self.islogged = None
        self.hashed = None
        self.path = None
        self.new_user = None

    # def insert(self):
    #     print("insert only")
    #     Session = sessionmaker(bind=UserManager.engine)
    #     session = Session()
    #     new_user = users_model.User("john12", "blabla")
    #     session.add(new_user)
    #     session.commit()


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
        self.islogged = False

        while not self.islogged:
            userdata = []
            with open('users.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    userdata.append(row)
            self.name = input('Podaj swój login: ')
            self.password = getpass.getpass('Podaj swoje hasło ')
            col0 = [x[0] for x in userdata]
            col1 = [x[1] for x in userdata]
            if self.name in col0:
                for k in range(0, len(col0)):
                    if col0[k] == self.name and col1[k] == bcrypt.checkpw(self.password, self.hashed):
                        print("Zalogowałeś się ")
                        self.islogged = True
            else:
                print('Nieprawidłowy login lub hasło')
                print('Spróbuj się zarejestrować')
                self.register()
        self.options()

    def verifyLogin(self, name):
        csv_file = csv.reader(open("users.csv", "r"))
        if not any(char.isdigit() for char in name):
            print('Podaj choć jedną cyfrę w loginie użytkownika')
            self.register()
        else:
            while True:
                for row in csv_file:
                    if name == row[0]:
                        print("Użytkownik o takim loginie już istnieje")
                        print("Zarejestruj się jako nowy użytkownik o innym loginie")
                        self.register()
                break



    def options(self):
        while self.islogged:
            print("Witamy w programie logowania\n")
            print("Wybierz opcję menu lista: 1/szukaj: 2/usun: 3/zakoncz: 4\n")
            menu = int(input("podaj wybór: "))
            if menu == 1:
                self.displayUsers()
            elif menu == 2:
                self.searchByLogin()
            elif menu == 3:
                self.deleteEntry()
                print("Wybrany użytkownik został usunięty z rejestru, tej operacji nie można odwrócić")
            else:
                exit()


