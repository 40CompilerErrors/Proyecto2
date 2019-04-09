from Controllers import UserController as UC
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow

class UserMenu(QMainWindow):

    def __init__(self):
        super(UserMenu, self).__init__()
        self.controller = UC.UserController(self)
        loadUi('./Resources/UI/VentanaUsuario.ui', self)

        self.boton_classifyfiles.clicked.connect(self.__callClass)
        self.boton_classifyweb.clicked.connect(self.__callWebClass)

        self.setWindowTitle('Pantalla Usuario')


    def __callClass(self):
        print("llego1")
        self.controller.openClass()

    def __callWebClass(self):
        self.controller.openWebClass()

