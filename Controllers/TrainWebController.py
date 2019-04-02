from Views import TrainWebMenu as TWM
import os
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget,QTableWidget,QGridLayout,QTableWidgetItem,QFileDialog, QLabel

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
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
import requests
import re
from bs4 import BeautifulSoup


class TrainWebController:

    def __init__(self, view):
        self.view = view
        self.linkList = []
        self.categoryList = []
        self.addedList = []
        self.starList = []
        self.contentList = []
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

    def addURL(self):
        self.link = self.view.lineEdit_URL.text()
        print(self.link)
        '''if re.search("https://www.metacritic.com/game/.*/.*", self.link):
            print("It's a game")
        elif re.search("https://www.metacritic.com/music/.*/.*", self.link):
            print("It's music")
        elif re.search("https://www.metacritic.com/tv/.*", self.link):
            print("It's a tv show")
        elif re.search("https://www.metacritic.com/movie/.*", self.link):
            print("It's a movie")
        else:
            print("Invalid syntax")'''
        self.linkList.append(self.link)
        rowPosition = self.view.tableWidget.rowCount()
        self.view.tableWidget.insertRow(rowPosition)
        self.view.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))
        self.view.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(self.link)))

    def metacritic(self, url):
        movie = False
        if re.search("https://www.metacritic.com/movie/.*", url):
            movie = True
            print("It's a movie")
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = page.content.decode('utf-8')
        page = page.replace("<br>", "\n")
        page = page.replace("<br/>", "\n")
        soup = BeautifulSoup(page, 'html.parser')
        if movie == True:

            userReviews = soup.find("a", string="User Score")
            userReviews = userReviews['href']
            userReviews = str(userReviews)

            url = "https://www.metacritic.com" + userReviews
            page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = page.content.decode('utf-8')
            page = page.replace("<br>", "\n")
            page = page.replace("<br/>", "\n")
            soup = BeautifulSoup(page, 'html.parser')
            html = list(soup.children)[2]
            reviewList = soup.findAll("div", {"class": "review"})

            pages = soup.find("div", {"class": "page_nav"})

            for i in range(len(reviewList)):
                star = reviewList[i].find("div", {"class": "metascore_w"})
                self.starList.append(float(star.text))
                content = reviewList[i].find("div", {"class": "review_body"})
                content = content.find("span")
                self.contentList.append(content.text)

            if pages:

                nextpage = soup.find("a", {"rel": "next"})

                while nextpage:
                    nextpage = nextpage['href']
                    url2 = "https://www.metacritic.com" + nextpage
                    page2 = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0'})
                    page2 = page2.content.decode('utf-8')
                    page2 = page2.replace("<br>", "\n")
                    page2 = page2.replace("<br/>", "\n")
                    soup2 = BeautifulSoup(page2, 'html.parser')
                    html2 = list(soup2.children)[2]
                    reviewList2 = soup2.findAll("div", {"class": "review"})

                    for i in range(len(reviewList2)):
                        star = reviewList2[i].find("div", {"class": "metascore_w"})
                        self.starList.append(float(star.text))
                        content = reviewList2[i].find("div", {"class": "review_body"})
                        content = content.find("span")
                        self.contentList.append(content.text)

                    nextpage = soup2.find("a", {"rel": "next"})
        else:
            criticReviews = soup.find("a", string="Critic Reviews")
            criticReviews = criticReviews['href']
            criticReviews = str(criticReviews)

            url1 = "https://www.metacritic.com" + criticReviews
            page1 = requests.get(url1, headers={'User-Agent': 'Mozilla/5.0'})
            page1 = page1.content.decode('utf-8')
            page1 = page1.replace("<br>", "\n")
            page1 = page1.replace("<br/>", "\n")
            soup1 = BeautifulSoup(page1, 'html.parser')
            html1 = list(soup1.children)[2]

            reviewList1 = soup1.findAll("li", {"class": "critic_review"})

            for i in range(len(reviewList1)):
                star = reviewList1[i].find("div", {"class": "metascore_w"})
                if star.text:
                    star = float(star.text)/10
                    self.starList.append(star)
                    content = reviewList1[i].find("div", {"class": "review_body"})
                    self.contentList.append(content.text)

            userReviews = soup.find("a", string="User Reviews")
            userReviews = userReviews['href']
            userReviews = str(userReviews)

            url2 = "https://www.metacritic.com" + userReviews
            page2 = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0'})
            page2 = page2.content.decode('utf-8')
            page2 = page2.replace("<br>", "\n")
            page2 = page2.replace("<br/>", "\n")
            soup2 = BeautifulSoup(page2, 'html.parser')
            html2 = list(soup2.children)[2]

            pages = soup2.find("ul", {"class": "pages"})

            reviewList2 = soup2.findAll("li", {"class": "user_review"})

            for j in range(len(reviewList2)):
                star = reviewList2[j].find("div", {"class": "metascore_w"})
                self.starList.append(float(star.text))
                content = reviewList2[j].find("div", {"class": "review_body"})
                self.contentList.append(content.text)

            if pages:

                nextpage = soup2.find("a", {"rel": "next"})

                while nextpage:
                    nextpage = nextpage['href']
                    url3 = "https://www.metacritic.com" + nextpage
                    page3 = requests.get(url3, headers={'User-Agent': 'Mozilla/5.0'})
                    page3 = page3.content.decode('utf-8')
                    page3 = page3.replace("<br>", "\n")
                    page3 = page3.replace("<br/>", "\n")
                    soup3 = BeautifulSoup(page3, 'html.parser')
                    html3 = list(soup3.children)[2]

                    reviewList3 = soup3.findAll("li", {"class": "user_review"})

                    for h in range(len(reviewList3)):
                        star = reviewList3[h].find("div", {"class": "metascore_w"})
                        self.starList.append(float(star.text))
                        content = reviewList3[h].find("div", {"class": "review_body"})
                        self.contentList.append(content.text)

                    nextpage = soup3.find("a", {"rel": "next"})
            category_number = self.view.comboBox_categorias.currentText()
            print(self.starList[-1])
            print(self.contentList[-1])
        if category_number == '2':
            self.categoryList = [self.view.lineEdit_cat1.text(),self.view.lineEdit_cat2.text()]
            for i in range(len(self.starList)):
                if self.starList[i] > 5:
                    self.labels.append('0')
                else:
                    self.labels.append('1')
        elif category_number == '3':
            self.categoryList = [self.view.lineEdit_cat1.text(), self.view.lineEdit_cat2.text(),
                                 self.view.lineEdit_cat3.text()]
            for i in range(len(self.starList)):
                if self.starList[i] >= 0 and self.starList[i] <= 3.3 :
                    self.labels.append('0')
                elif self.starList[i] > 3.3 and self.starList[i] <= 6.6 :
                    self.labels.append('1')
                else:
                    self.labels.append('2')
        elif category_number == '4':
            self.categoryList = [self.view.lineEdit_cat1.text(), self.view.lineEdit_cat2.text(),
                                 self.view.lineEdit_cat3.text(), self.view.lineEdit_cat4.text()]
            for i in range(len(self.starList)):
                if self.starList[i] >= 0 and self.starList[i] <= 2.5 :
                    self.labels.append('0')
                elif self.starList[i] > 2.5 and self.starList[i] <= 5 :
                    self.labels.append('1')
                elif self.starList[i] > 5 and self.starList[i] <= 7.5 :
                    self.labels.append('2')
                else:
                    self.labels.append('3')
        elif category_number == '5':
            self.categoryList = [self.view.lineEdit_cat1.text(), self.view.lineEdit_cat2.text(),
                                 self.view.lineEdit_cat3.text(), self.view.lineEdit_cat4.text(),
                                 self.view.lineEdit_cat5.text()]
            for i in range(len(self.starList)):
                if self.starList[i] >= 0 and self.starList[i] <= 2 :
                    self.labels.append('0')
                elif self.starList[i] > 2 and self.starList[i] <= 4 :
                    self.labels.append('1')
                elif self.starList[i] > 4 and self.starList[i] <= 6 :
                    self.labels.append('2')
                elif self.starList[i] > 6 and self.starList[i] <= 8 :
                    self.labels.append('3')
                else:
                    self.labels.append('4')

        print(self.categoryList)



    def webscrapper_train(self):


        print("Ejecutando el entrenador...")
        nltk.download('stopwords')
        stemmer = PorterStemmer()
        print('llego1')

        X, y = self.contentList, self.labels
        print('llego2')
        #self.nombre_etiquetas = valoraciones.target_names
        documentos = []
        print('llego3')
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
        print(documentos)


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
        #ME HE QUEDADO AQUI
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
    def choose_algorithm(self):
        self.algorithm_name = str(self.view.comboBox_algoritmos.currentText())

        if self.algorithm_name == 'Random Forest':
            self.algorithm = RandomForestClassifier(n_estimators=1000, random_state=0)

        elif self.algorithm_name == 'Naive Bayes':
            self.algorithm = GaussianNB()

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
