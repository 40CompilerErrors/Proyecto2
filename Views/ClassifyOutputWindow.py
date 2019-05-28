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
        self.initiateVariables()
        self.buttonActions()

    def initiateVariables(self):
        pass
        # self.label_finalizado.setVisible(False)
        # self.webs_list = ['Amazon', 'Steam', 'Metacritic', 'Yelp']
        # for i in self.webs_list:
        #     self.pages_combo.addItem(i)

        # def nextWindow(self):
        #     self.controller.switch_view(

    def buttonActions(self):
        self.save_button.clicked.connect(self.controller.saveResults)
        self.backButton.clicked.connect(self.controller.goBack)
        # self.removeButton.clicked.connect(self.controller.removeReviews)
        # self.addFolderButton.clicked.connect(self.controller.addFromFile)
        # self.getModelsButton.clicked.connect(self.controller.downloadModels)


