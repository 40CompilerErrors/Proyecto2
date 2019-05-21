import sys

from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from Controllers import LoginController as MC


class LoginMenu(QMainWindow):

    # metodo para iniciar la clase VentanaInicio
    def __init__(self):
        super(LoginMenu, self).__init__()

        self.controller = MC.LoginController(self)

        loadUi('./Resources/UI/VentanaLogin.ui', self)

        pixmap = QPixmap('./Resources/UIElements/logo.jpeg')
        self.logo.setPixmap(pixmap)
        self.setWindowTitle('Pantalla Login')
        self.login_button.clicked.connect(self.__login)
        self.label_errors.setVisible(False)
        #self.login_button.setShortcut("Intro")    esto pone el atajo al teclado pero tengo que revisarlo

    def __login(self):
        user = self.user_text.text()
        password = self.pass_text.text()
        self.controller.user_access(user, password)



