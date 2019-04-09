from Controllers import AdminController as AC
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
import numpy as np


class AdminUsers(QMainWindow):
    
    lista = []

    def __init__(self):
        super(AdminUsers, self).__init__()
        self.controller = AC.AdminController(self)
        loadUi('./Resources/UI/VentanaUsuarios.ui', self)

       
        self.pushButton.clicked.connect(self.__login)

        self.setWindowTitle('Pantalla Gestion Admin')
        result = self.controller.getUser()
        print(result)
        lista = result
        print(lista)
        #self.comboBox.addItems(lista)
       

    """
    def __abrir(self):
        self.controller.openTrainer()

    def __abrirweb(self):
        self.controller.openWebScrapper()
        
    """
    
    
    
    def __test(self):
        print("toz")
        
    def __login(self):
        newUser = self.lineEdit_3.text()
        newPassword = self.lineEdit_4.text()
        self.controller.insertUser(newUser, newPassword)
        
        
        
        