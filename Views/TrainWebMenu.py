from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from Controllers import TrainWebController as TWC

class TrainWebMenu(QMainWindow):

    def __init__(self):
        super(TrainWebMenu, self).__init__()

        self.controller = TWC.TrainWebController(self)
        self.webs_list = []
        self.category_list = []

        loadUi('./Resources/UI/VentanaEntrenamientoWeb.ui', self)

        self.setWindowTitle('Pantalla de entrenador web')

        self.initiateVariables()
        self.buttonActions()

    def initiateVariables(self):
        self.webs_list = ['Amazon', 'Steam', 'Metacritic']
        self.category_list = ['3','2','4','5']
        for i in self.webs_list:
            self.comboBox_websites.addItem(i)
        for i in self.category_list:
            self.comboBox_categorias.addItem(i)

    def buttonActions(self):
        self.pushButton_addUrl.clicked.connect(self.controller.addURL)
        self.boton_scraper.clicked.connect(self.call_scrapper)
        self.comboBox_categorias.currentTextChanged.connect()

    def call_scrapper(self):
        self.controller.metacritic(self.controller.linkList[0])