from Controllers import AdminController as AC
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow


class AdminMenu(QMainWindow):

    def __init__(self):
        super(AdminMenu, self).__init__()

        self.controller = AC.AdminController(self)

        loadUi('./Resources/UI/VentanaAdmin.ui', self)

        self.boton_trainfiles.clicked.connect(self.__abrir)

        self.setWindowTitle('Pantalla Admin')

    def __abrir(self):
        self.controller.openTrainer()
