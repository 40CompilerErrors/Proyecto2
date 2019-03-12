from Views import UserMenu as UM, AdminMenu as AM
import main as m


class MainController:

    def __init__(self, view):
        self.view = view


    def user_access(self, username, password):

        if self.__validate(username, password) == "admin":
            self.view.running = False
            m.current = AM.AdminMenu()
            return True
        elif self.__validate(username, password) == "user":
            self.view.running = False
            m.current = UM.UserMenu()
            return True
        else:
            pass


    def __validate(self, username, password):
        # There will be validation here later on
        #PLACEHOLDER METHOD
        return username

