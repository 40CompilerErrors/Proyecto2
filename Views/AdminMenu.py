from Controllers import AdminController as AC
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow


class AdminMenu(QMainWindow):

    def __init__(self):
        super(AdminMenu, self).__init__()
        self.controller = AC.AdminController(self)
        loadUi('./Resources/UI/VentanaAdmin.ui', self)

        self.boton_trainweb.clicked.connect(self.__abrirweb)
        self.boton_usersAdmin.clicked.connect(self.__abrirgestor)
       

        self.setWindowTitle('Pantalla Admin')

    def __abrirweb(self):
        self.controller.openWebScrapper()
        
    def __abrirgestor(self):
        self.controller.openGestor()
        
    