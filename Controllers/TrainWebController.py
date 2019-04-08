
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget,QTableWidget,QGridLayout,QTableWidgetItem,QFileDialog, QLabel

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

import nltk
import matplotlib.pyplot as plt

from sklearn.datasets import load_files
import pickle
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer
from PyQt5.QtWidgets import QTableWidgetItem
import re
from Model.Scrappers import MetacriticScrapper as MS, AmazonScrapper as AS, SteamScrapper as SS, YelpScrapper as YS
from Model import DB_Driver as DB


class TrainWebController:


    def __init__(self, view):
        self.view = view
        self.linkList = []
        self.starList = []
        self.contentList = []
        self.categoryList = []
        self.addedList = []
        self.labels = []
        '''
        Estos array estan por si acaso 
        self.vgood = []
        self.good = []
        self.neutral = []
        self.bad = []
        self.vbad = []
        '''
        self.algorithm = ''
        self.algorithm_name = ''
        self.stopword = ''
        self.i = 0
        self.j = 0
        self.h = 0

    def validate(self):
        if 'metacritic' in self.view.lineEdit_URL.text() and self.view.comboBox_websites.currentText() == 'Metacritic':
            self.addURL()
            self.view.label_formatError.setVisible(False)
        elif 'steam' in self.view.lineEdit_URL.text() and self.view.comboBox_websites.currentText() == 'Steam':
            self.addURL()
            self.view.label_formatError.setVisible(False)
        elif 'amazon' in self.view.lineEdit_URL.text() and self.view.comboBox_websites.currentText() == 'Amazon':
            self.addURL()
            self.view.label_formatError.setVisible(False)
        elif 'yelp' in self.view.lineEdit_URL.text() and self.view.comboBox_websites.currentText() == 'Yelp':
            self.addURL()
            self.view.label_formatError.setVisible(False)
        else:
            self.view.label_formatError.setVisible(True)

    def addURL(self):
        link = self.view.lineEdit_URL.text()
        self.linkList.append(link)
        rowPosition = self.view.tableWidget.rowCount()
        self.view.tableWidget.insertRow(rowPosition)
        self.view.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))
        self.view.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(link)))
        self.view.lineEdit_URL.setText("")


    def scrapLinks(self):
        metacriticScrapper = MS.MetacriticScrapper()
        steamScrapper = SS.SteamScrapper()
        yelpScrapper = YS.YelScrapper()
        amazonScrapper = AS.AmazonScrapper()

        for url in self.linkList:
            print("Scrapping link: " + url)
            url_stars, url_reviews = [],[]
            if 'metacritic.com' in url:
                url_stars, url_reviews = metacriticScrapper.scrapURL(url)
            elif 'store.steampowered.com' in url:
                url_stars, url_reviews = steamScrapper.scrapURL(url)
            elif 'amazon.com' in url:
                url_stars, url_reviews = amazonScrapper.scrapURL(url)
            elif 'yelp.com/biz' in url:
                url_stars, url_reviews = yelpScrapper.scrapURL(url)

            self.starList += url_stars
            self.contentList += url_reviews

    def guardar_modelo(self):
        nombre_modelo = self.view.modelName_text.text()


        # Aqui guardamos el Modelo en formato pickle
        with open(f'./Resources/Models/{nombre_modelo}', 'wb') as modelo_completo:
             pickle.dump(self.algorithm, modelo_completo)
             pickle.dump(self.vectorizador, modelo_completo)
             pickle.dump(self.labels, modelo_completo)

        db = DB.DB_Driver()

        db.uploadModel(nombre_modelo)

        db.closeConnection()

        self.view.label_guardarModelo.setVisible(True)


    def __starsToCategories(self):
        category_number = self.view.comboBox_categorias.currentText()

        if category_number == '2':
            self.categoryList = [self.view.lineEdit_cat1.text() ,self.view.lineEdit_cat2.text()]
            for item in self.starList:
                value = int(item)
                if value < 4:   #Originally >3 but it seemed so weird to invert the order here, so I assumed it was a bug
                    self.labels.append('1')
                else:
                    self.labels.append('0')

        elif category_number == '3':
            self.categoryList = [self.view.lineEdit_cat1.text(), self.view.lineEdit_cat2.text(),
                                 self.view.lineEdit_cat3.text()]
            for item in self.starList:
                value = int(item)
                if value < 2:
                    self.labels.append('2')
                elif value < 4:
                    self.labels.append('1')
                else:
                    self.labels.append('0')

        elif category_number == '4':
            self.categoryList = [self.view.lineEdit_cat1.text(), self.view.lineEdit_cat2.text(),
                                 self.view.lineEdit_cat3.text(), self.view.lineEdit_cat4.text()]
            for item in self.starList:
                value = int(item)
                if value < 4 :
                    self.labels.append('3')
                elif value < 6:
                    self.labels.append('2')
                elif value < 8:
                    self.labels.append('1')
                else:
                    self.labels.append('0')

        elif category_number == '5':
            self.categoryList = [self.view.lineEdit_cat1.text(), self.view.lineEdit_cat2.text(),
                                 self.view.lineEdit_cat3.text(), self.view.lineEdit_cat4.text(),
                                 self.view.lineEdit_cat5.text()]

            for item in self.starList:
                value = int(item)
                if value <3 : #A heart!
                    self.labels.append('4')
                elif value < 5 :
                    self.labels.append('3')
                elif value < 7:
                    self.labels.append('2')
                elif value < 9 :
                    self.labels.append('1')
                else:
                    self.labels.append('0')

    def webscrapper_train(self):

        self.__starsToCategories()

        print("Ejecutando el entrenador...")
        nltk.download('stopwords')
        stemmer = PorterStemmer()

        X, y = self.contentList, self.labels

        #self.nombre_etiquetas = valoraciones.target_names
        documentos = []
        self.stopword = str(self.view.comboBox_stopwords.currentText())
        for sen in range(0, len(X)):
            # Elimina: carácteres especiales
            documento = re.sub(r'\W', ' ', str(X[sen]))

            # Elimina: carácteres solos
            # remove all single characters
            documento = re.sub(r'\s+[a-zA-Z]\s+', ' ', documento)

            # Elimina: números
            documento = re.sub(r'\d', ' ', documento)

            # Elimina: carácteres solos al principio de una línea.
            documento = re.sub(r'\^[a-zA-Z]\s+', ' ', documento)

            # Sustituye: los tabuladores o multiples espacios por un solo espacio
            documento = re.sub(r'\s+', ' ', documento, flags=re.I)

            # Removing prefixed 'b'
            documento = re.sub(r'^b\s+', '', documento)

            # Convierte todas las mayusuculas a minúsculas
            documento = documento.lower()

            # Hacemos el Stem para sacar las raices de cada una de las palabras
            documento = documento.split()

            documento = [stemmer.stem(word) for word in documento]
            documento = ' '.join(documento)

            documentos.append(documento)
        self.vectorizador = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words(self.stopword))

        # Almacenamos las palabras en su respectivo formato numerico en X
        X = self.vectorizador.fit_transform(documentos).toarray()

        X_entrenamiento, X_test, y_entrenamiento, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        self.choose_algorithm()

        self.algorithm.fit(X_entrenamiento, y_entrenamiento)
        y_pred = self.algorithm.predict(X_test)
        matriz_confusion = confusion_matrix(y_test, y_pred)

        figura = plt.figure()
        ax = figura.add_subplot(111)

        cmap = plt.get_cmap('Blues')
        cax = ax.matshow(matriz_confusion, interpolation='nearest', cmap=cmap)
        figura.colorbar(cax)

        etiquetas = np.arange(len(self.categoryList))
        plt.xticks(etiquetas, self.categoryList, rotation=45)
        plt.yticks(etiquetas, self.categoryList)

        fmt = '.2f'
        thresh = matriz_confusion.max() / 2.
        for i, j in itertools.product(range(matriz_confusion.shape[0]), range(matriz_confusion.shape[1])):
            plt.text(j, i, format(matriz_confusion[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if matriz_confusion[i, j] > thresh else "black")

        plt.xlabel('Predicted')
        plt.ylabel('True')
        figura.savefig('./Resources/UIElements/Matriz.png')
        print("Imagen guardada")

        label = QLabel(self.view)
        pixmap = QPixmap('./Resources/UIElements/Matriz.png')
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.show()
        self.view.lay.addWidget(label)

        true_positive = matriz_confusion[0][0]
        false_positive = matriz_confusion[0][1]
        false_negative = matriz_confusion[1][0]
        true_negative = matriz_confusion[1][1]

        print(matriz_confusion)
        print(classification_report(y_test, y_pred))
        self.precision = accuracy_score(y_test, y_pred)


        print('True positive = ', true_positive)
        print('False positive = ', false_positive)
        print('False negative = ', false_negative)
        print('True negative = ', true_negative)
        print(self.precision)
        self.view.label_precision.setVisibleU(True)


    def choose_algorithm(self):
        self.algorithm_name = str(self.view.comboBox_algoritmos.currentText())

        if self.algorithm_name == 'Random Forest':
            self.algorithm = RandomForestClassifier(n_estimators=1000, random_state=0)

        elif self.algorithm_name == 'Naive Bayes':
            self.algorithm = GaussianNB()

    #def save_model(self):


    def change_category_combo(self):

        category_number = str(self.view.comboBox_categorias.currentText())

        if category_number == '2':
            self.categoryList = [self.view.lineEdit_cat1.text(), self.view.lineEdit_cat2.text()]
            self.view.lineEdit_cat1.setText('Buenas')
            self.view.lineEdit_cat2.setText('Malas')
            self.view.label_12.setVisible(False)
            self.view.lineEdit_cat3.setVisible(False)
            self.view.label_13.setVisible(False)
            self.view.lineEdit_cat4.setVisible(False)
            self.view.label_14.setVisible(False)
            self.view.lineEdit_cat5.setVisible(False)


        elif category_number == '3':
            self.view.lineEdit_cat1.setText('Buenas')
            self.view.lineEdit_cat2.setText('Neutras')
            self.view.lineEdit_cat3.setText('Malas')
            self.view.label_12.setVisible(True)
            self.view.lineEdit_cat3.setVisible(True)
            self.view.label_13.setVisible(False)
            self.view.lineEdit_cat4.setVisible(False)
            self.view.label_14.setVisible(False)
            self.view.lineEdit_cat5.setVisible(False)


        elif category_number == '4':
            self.view.lineEdit_cat1.setText('Muy Buenas')
            self.view.lineEdit_cat2.setText('Buenas')
            self.view.lineEdit_cat3.setText('Malas')
            self.view.lineEdit_cat4.setText('Muy Malas')
            self.view.label_12.setVisible(True)
            self.view.lineEdit_cat3.setVisible(True)
            self.view.label_13.setVisible(True)
            self.view.lineEdit_cat4.setVisible(True)
            self.view.label_14.setVisible(False)
            self.view.lineEdit_cat5.setVisible(False)



        elif category_number == '5':
            self.view.lineEdit_cat1.setText('Muy Buenas')
            self.view.lineEdit_cat2.setText('Buenas')
            self.view.lineEdit_cat3.setText('Neutras')
            self.view.lineEdit_cat4.setText('Malas')
            self.view.lineEdit_cat5.setText('Muy Malas')
            self.view.label_12.setVisible(True)
            self.view.lineEdit_cat3.setVisible(True)
            self.view.label_13.setVisible(True)
            self.view.lineEdit_cat4.setVisible(True)
            self.view.label_14.setVisible(True)
            self.view.lineEdit_cat5.setVisible(True)



        ''' IMPORTANTE, ESTO HAY QUE METERLO EN EL ENTRENADOR EN CUANTO PODAMOS
        
        sno = nltk.stem.SnowballStemmer(self.view.comboBox_stopwords.currentText())
        print('llego4')

        for item in X:
            item2 = item.decode('utf-8')
            item2 = item2.lower()
            item2 = word_tokenize(item2)
            item2 = [w for w in item2 if not w in self.stopword]
            frase_stemming = []
            for w in item2:
                if w not in self.stopword:
                    frase_stemming.append(sno.stem(w))
            item2 = frase_stemming
            documentos.append(item2)
        print('llego5')

        documentos = [str (item) for item in documentos]
        '''
        
        
if __name__ == "__main__":
    pass
