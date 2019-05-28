from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from Controllers import ClassifyController as CWC
from Views import ClassifyOutputWindow as COWa

class ClassifyInputWindow(QMainWindow):
    def __init__(self,controller):
        super(ClassifyInputWindow, self).__init__()
        self.controller = controller
        loadUi('./Resources/UI/InputWindowClasificadorWeb.ui', self)

        self.webs_list = []

        self.setWindowTitle('Ventana Clasificador')
        self.initiateVariables()
        self.buttonActions()


    def initiateVariables(self):
        # self.label_finalizado.setVisible(False)
        self.webs_list = ['Amazon', 'Steam', 'Metacritic', 'Yelp']
        for i in self.webs_list:
            self.pages_combo.addItem(i)



    def buttonActions(self):
        pass
        self.addUrl_button.clicked.connect(self.controller.validate)
        #self.save_button.clicked.connect(self.controller.obtainRoute)
        self.boton_clasificador.clicked.connect(self.controller.ejecutar_clasificador)
        self.removeButton.clicked.connect(self.controller.removeReviews)
        self.addFolderButton.clicked.connect(self.controller.addFromFile)
        self.getModelsButton.clicked.connect(self.controller.downloadModels)
