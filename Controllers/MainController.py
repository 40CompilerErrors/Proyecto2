from Views import UserMenu as UM, AdminMenu as AM,MainMenu as MM
from main import Main as m


class MainController:

    def __init__(self, view):
        self.view = view

    def user_access(self, username, window):

        if username == "admin":
            self.view.running = False
            adminWindow = AM.AdminMenu()
            adminWindow.show()
            window.close()

        elif username == "user":
            self.view.running = False
            m.change_current(UM.UserMenu())

    def __validate(self, username,password):
        return username
