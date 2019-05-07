from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from Controllers import ClassifyWebController as CWC

class ClassifyWebMenu(QMainWindow):
    def __init__(self):
        super(ClassifyWebMenu, self).__init__()
        self.controller = CWC.ClassifyWebController(self)
        loadUi('./Resources/UI/VentanaClasificadorWeb.ui', self)

        self.webs_list = []

        self.setWindowTitle('Ventana Clasificador')
        self.initiateVariables()
        self.buttonActions()
        self.controller.obtainModels()

    def initiateVariables(self):
        self.label_finalizado.setVisible(False)
        self.webs_list = ['Amazon', 'Steam', 'Metacritic', 'Yelp']
        for i in self.webs_list:
            self.pages_combo.addItem(i)

    def buttonActions(self):
        self.addUrl_button.clicked.connect(self.controller.validate)
        self.save_button.clicked.connect(self.controller.obtainRoute)
        self.boton_clasificador.clicked.connect(self.controller.ejecutar_clasificador)
        self.removeButton.clicked.connect(self.controller.removeReviews)
        self.addFolderButton.clicked.connect(self.controller.addFromFile)


