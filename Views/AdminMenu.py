from Controllers import AdminController as AC
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow


class AdminMenu(QMainWindow):

    def __init__(self,controller):
        super(AdminMenu, self).__init__()

        self.controller = controller
        loadUi('./Resources/UI/AdminMenu.ui', self)

        self.setWindowTitle('Pantalla Admin')

        self.initiateVariables()
        self.buttonActions()


    def initiateVariables(self):

        self.stopwords_list = ['english', 'danish', 'dutch', 'arabic', 'finnish', 'french', 'german', 'hungarian',
                                   'italian', 'kazakh', 'norwegian', 'portuguese', 'romanian', 'russian', 'spanish',
                                   'swedish', 'turkish']
        self.webs_list = ['Amazon', 'Steam', 'Metacritic', 'Yelp']
        self.category_list = ['3','2','4','5']
        self.algorithm_list = ['Random Forest', 'Naive Bayes', 'SVM']

        # self.webs_list = []
        # self.category_list = []
        # self.stopwords_list = []
        # self.algorithm_list = []

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
        self.label_formatError.setVisible(False)
        self.labelError1.setVisible(False)

        self.password_error.setVisible(False)
        self.user_error.setVisible(False)

    def buttonActions(self):
        self.pushButton_addUrl.clicked.connect(self.controller.validate)
        # self.boton_scraper.clicked.connect(self.call_scrapper)
        self.comboBox_categorias.currentTextChanged.connect(self.controller.change_category_combo)
        self.boton_clasificador_.clicked.connect(self.controller.webscrapper_train)
        # self.boton_guardarModelo_.clicked.connect(self.controller.guardar_modelo)
        self.boton_algoritmos_1.clicked.connect(self.controller.editar_algoritmo)
        self.boton_ruta.clicked.connect(self.controller.addfromfile)

        self.pushButton.clicked.connect(self.crearUsuario)
        self.pushButton_2.clicked.connect(self.borrar)


    def crearUsuario(self):
        newUser = self.lineEdit_3.text()
        newPassword = self.lineEdit_4.text()
        self.user_error.setVisible(False)
        self.password_error.setVisible(False)
        if newUser!="" and newPassword!="":
             self.controller.insertUser(newUser, newPassword)
        elif newUser=="":
             self.user_error.setText('Invalid user , please introduce a valid user.')
             self.user_error.setVisible(True)
        elif newPassword=="":
             self.password_error.setText('Invalid password , please introduce a valid password.')
             self.password_error.setVisible(True)
       

        self.userTable.setRowCount(0)
        self.comboBox.clear()
        self.controller.loadUsers()

        # result = self.controller.getUser()
        # listaUsers = []
        # for i in result:
        #     listaUsers.append(i[0])
        #
        # self.comboBox.addItems(listaUsers)

    def borrar(self):
        oldUser = self.comboBox.currentText()
        self.controller.borrarUsuario(oldUser)

        self.userTable.setRowCount(0)
        self.comboBox.clear()
        self.controller.loadUsers()

        # result = self.controller.getUser()
        # listaUsers = []
        # for i in result:
        #     listaUsers.append(i[0])
        #
        # self.comboBox.addItems(listaUsers)