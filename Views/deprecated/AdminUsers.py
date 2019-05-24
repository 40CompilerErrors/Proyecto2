from Controllers import AdminController as AC
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
import numpy as np


class AdminUsers(QMainWindow):
    
    

    def __init__(self):
        super(AdminUsers, self).__init__()
        self.controller = AC.AdminController(self)
        loadUi('./Resources/UI/VentanaUsuarios.ui', self)

       
        self.pushButton.clicked.connect(self.crearUsuario)
        self.pushButton_2.clicked.connect(self.borrar)
        

        self.setWindowTitle('Pantalla Gestion Admin')
        result = self.controller.getUser()
        listaUsers = []
        for i in result:
            listaUsers.append(i[0])
            
        self.comboBox.addItems(listaUsers)
            
        
    def crearUsuario(self):
        newUser = self.lineEdit_3.text()
        newPassword = self.lineEdit_4.text()
        self.controller.insertUser(newUser, newPassword)
        
        self.tableWidget.setRowCount(0)
        self.comboBox.clear()
        result = self.controller.getUser()
        listaUsers = []
        for i in result:
            listaUsers.append(i[0])
            
        self.comboBox.addItems(listaUsers)
        
        
    def borrar(self):
        oldUser = self.comboBox.currentText()
        self.controller.borrarUsuario(oldUser)
        
        self.tableWidget.setRowCount(0)
        self.comboBox.clear()
        result = self.controller.getUser()
        listaUsers = []
        for i in result:
            listaUsers.append(i[0])
            
        self.comboBox.addItems(listaUsers)
        
        
        
        