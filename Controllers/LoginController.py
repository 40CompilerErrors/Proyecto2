from Controllers import ClassifyController as CWC, AdminController as AC
from Model import User as US


class LoginController:

    def __init__(self, view):
        self.view = view

    def user_access(self, username, password):

        valid, role = US.User().validate(username,password)

        if valid != True:
            if role == 1:
                print("Validation failed: Password incorrect")
                self.view.label_errors.setVisible(True)
            else:
                print("Validation failed: No user found")
                self.view.label_errors.setVisible(True)

        elif valid and role == 0:
            self.view.running = False
            classifier = CWC.ClassifyWebController()
            self.view.close()

        elif valid and role == 1:

            self.view.running = False
            adminMenu = AC.AdminController()
            self.view.close()










