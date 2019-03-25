from Views import UserMenu as UM, AdminMenu as AM
from main import Main as m
import sys

class MainController:

    def __init__(self, view):
        self.view = view

    def user_access(self, username):

        if username == "admin":
            self.view.running = False
            print('llego')
            ventanaAdmin = AM.AdminMenu()
            ventanaAdmin.show()
            # m.change_current(AM.AdminMenu())

        elif username == "user":
            self.view.running = False
            m.change_current(UM.UserMenu())

    def __validate(self, username,password):
        return username
