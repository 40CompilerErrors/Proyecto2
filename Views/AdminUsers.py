from Controllers import AdminController as AC
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow


class AdminUsers(QMainWindow):

    def __init__(self):
        super(AdminUsers, self).__init__()
        self.controller = AC.AdminController(self)
        loadUi('./Resources/UI/VentanaUsuarios.ui', self)

       
       

        self.setWindowTitle('Pantalla Gestion Admin')


"""
    def __abrir(self):
        self.controller.openTrainer()

    def __abrirweb(self):
        self.controller.openWebScrapper()
        
    """
    