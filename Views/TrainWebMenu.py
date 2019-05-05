from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from Controllers import TrainWebController as TWC

class TrainWebMenu(QMainWindow):

    def __init__(self):
        super(TrainWebMenu, self).__init__()

        self.controller = TWC.TrainWebController(self)
        self.webs_list = []
        self.category_list = []
        self.stopwords_list = []
        self.algorithm_list = []

        loadUi('./Resources/UI/VentanaEntrenamientoWeb.ui', self)

        self.setWindowTitle('Pantalla de entrenador web')




        self.initiateVariables()
        self.buttonActions()

    def initiateVariables(self):

        self.stopwords_list = ['english', 'danish', 'dutch', 'arabic', 'finnish', 'french', 'german', 'hungarian',
                                   'italian', 'kazakh', 'norwegian', 'portuguese', 'romanian', 'russian', 'spanish',
                                   'swedish', 'turkish']
        self.webs_list = ['Amazon', 'Steam', 'Metacritic', 'Yelp']
        self.category_list = ['3','2','4','5']
        self.algorithm_list = ['Random Forest', 'Naive Bayes', 'SVM']

        for i in self.algorithm_list:
            self.comboBox_algoritmos.addItem(i)
        for i in self.webs_list:
            self.comboBox_websites.addItem(i)
        for i in self.category_list:
            self.comboBox_categorias.addItem(i)
        for i in self.stopwords_list:
            self.comboBox_stopwords.addItem(i)
        self.lineEdit_cat1.setText('Buenas')
        self.lineEdit_cat2.setText('Neutras')
        self.lineEdit_cat3.setText('Malas')
        self.label_13.setVisible(False)
        self.label_14.setVisible(False)
        self.lineEdit_cat4.setVisible(False)
        self.lineEdit_cat5.setVisible(False)
        self.label_precision.setVisible(False)
        self.label_guardarModelo.setVisible(False)
        self.label_formatError.setVisible(False)
        self.labelError1.setVisible(False)


    def buttonActions(self):
        self.pushButton_addUrl.clicked.connect(self.controller.validate)
        self.boton_scraper.clicked.connect(self.call_scrapper)
        self.comboBox_categorias.currentTextChanged.connect(self.controller.change_category_combo)
        self.boton_clasificador.clicked.connect(self.controller.webscrapper_train)
        self.boton_guardarModelo.clicked.connect(self.controller.guardar_modelo)
        self.boton_algoritmos.clicked.connect(self.controller.editar_algoritmo)

    def call_scrapper(self):
        self.controller.scrapLinks()