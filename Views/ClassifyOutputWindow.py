from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from Controllers import ClassifyController as CWC
from Views import ClassifyInputWindow as CIW

class ClassifyOutputWindow(QMainWindow):
    def __init__(self,controller):
        super(ClassifyOutputWindow, self).__init__()
        self.controller = controller
        loadUi('./Resources/UI/OutputWindowClasificadorWeb.ui', self)

        self.webs_list = []

        self.setWindowTitle('Ventana Clasificador')
        self.buttonActions()

    def buttonActions(self):
        self.save_button.clicked.connect(self.controller.saveResults)
        self.backButton.clicked.connect(self.controller.goBack)

