from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from Controllers import ClassifyWebController as CWC

class ClassifyWebMenu(QMainWindow):
    def __init__(self):
        super(ClassifyWebMenu, self).__init__()
        self.controller = CWC.ClassifyWebController(self)
        loadUi('./Resources/UI/VentanaClasificadorWeb.ui', self)
        self.setWindowTitle('Ventana Clasificador')