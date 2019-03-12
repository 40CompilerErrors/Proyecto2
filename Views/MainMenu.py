import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from Controllers import MainController as MC


class MainMenu(QMainWindow):

    # metodo para iniciar la clase VentanaInicio
    def __init__(self):
        super(MainMenu, self).__init__()

        self.controller = MC.MainController(self)

        loadUi('./Resources/UI/VentanaInicio.ui', self)

        self.setWindowTitle('Pantalla Inicio')
        self.boton_clasificador.clicked.connect(self.__user_login)
        self.boton_entrenamiento.clicked.connect(self.__admin_login)
        self.setFixedSize(700,300)


    def __user_login(self):
        self.controller.user_access("user", "")

    def __admin_login(self):
        self.controller.user_access("admin", "")