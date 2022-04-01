from UserModule import User
import csv
import getpass


class LoggingApi:
    user = User

    def __init__(self):
        self.name = None
        self.password = None
        self.islogged = None

    def register(self):
        pattern = r'^[A-Z]{3}'
        print("Podaj login i hasło, aby się zarejestrować ")
        self.name = input("Podaj login w register, login musi zaczynać się trzema wielkimi literami i mieć jedną cyfrę: ")
        self.verifyLogin(self.name)
        while True:
            self.password = getpass.getpass("Podaj hasło o długości co najmniej 6 znaków z jedną cyfrą: ")
            if len(self.password) >= 6 and any(char.isdigit() for char in self.password):
                print("Poprawne hasło")
                break
            else:
                print("hasło musi mieć co najmniej 6 znaków i jedną cyfrę")
        with open('users.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([self.name, self.password])
            csvfile.close()
            print("Zarejestrowałeś się")
            self.islogged = True
        self.options()

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
                    if col0[k] == self.name and col1[k] == self.password:
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

    def deleteEntry(self):
        lines = list()
        name = input("Podaj login do usunięcia: ")
        with open('users.csv', 'r+', newline='') as in_file:
            # rows = [row for row in csv.reader(in_file) if member_name not in row]
            # in_file.seek(0)
            # writer = csv.writer(in_file)
            # writer.writerows(rows)
            reader = csv.reader(in_file)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == name:
                        lines.remove(row)
        with open('users.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)






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

    def displayUsers(self):
        data = []
        with open("users.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
        print(data)

    def searchByLogin(self):
        login = str(input("Podaj login do wyszukania: \n"))
        csv_file = csv.reader(open("users.csv", "r"))
        for row in csv_file:
            if login == row[0]:
                print(row)
                break
            else:
                print("---------nie znaleziono----------")
