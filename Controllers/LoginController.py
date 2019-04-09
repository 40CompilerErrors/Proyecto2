from Views import UserMenu as UM, AdminMenu as AM, LoginMenu as MM
from main import Main as m
from Model import DB_Driver as DB
import hashlib, uuid


class LoginController:

    def __init__(self, view):
        self.view = view

    def user_access(self, username, password):

        valid, role = self.__validate(username,password)

        if valid != True:
            return

        if valid and role == 0:
            self.view.running = False
            userWindow = UM.UserMenu()
            userWindow.show()
            self.view.close()

        elif valid and role == 1:

            self.view.running = False
            adminWindow = AM.AdminMenu()
            adminWindow.show()
            self.view.close()


    def __validate(self, username,password):

        db = DB.DB_Driver()
        db_hash, db_role = db.getUser(username)
        db.closeConnection()

        if db_hash == 0 and db_role == 0:
            print("Validation failed: No user found")
            return False, 0

        hashed_password = hashlib.sha512(password.encode('utf8')).hexdigest()

        if not hashed_password == db_hash:
            print("Validation failed: Password incorrect")
            return False, 0
        else:
            return True, db_role








