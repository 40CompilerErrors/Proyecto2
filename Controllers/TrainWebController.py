from Views import TrainWebMenu as TWM
import os
import time

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
import requests
import re
from bs4 import BeautifulSoup


class TrainWebController:

    def __init__(self, view):
        self.view = view
        self.linkList = []
        self.addedList = []
        self.starList = []
        self.contentList = []
        self.algorithm = ''
        self.algorithm_name = ''
        self.vgood = []
        self.good = []
        self.neutral = []
        self.bad = []
        self.vbad = []
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
        soup = BeautifulSoup(page.content, 'html.parser')
        if movie == True:

            userReviews = soup.find("a", string="User Score")
            userReviews = userReviews['href']
            userReviews = str(userReviews)

            url = "https://www.metacritic.com" + userReviews
            page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(page.content, 'html.parser')
            html = list(soup.children)[2]
            reviewList = soup.findAll("div", {"class": "review"})

            pages = soup.find("div", {"class": "page_nav"})

            for i in range(len(reviewList)):
                star = reviewList[i].find("div", {"class": "metascore_w"})
                self.starList.append(star.text)
                content = reviewList[i].find("div", {"class": "review_body"})
                content = content.find("span")
                self.contentList.append(content.text)

            if pages:

                nextpage = soup.find("a", {"rel": "next"})

                while nextpage:
                    nextpage = nextpage['href']
                    url2 = "https://www.metacritic.com" + nextpage
                    page2 = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0'})
                    soup2 = BeautifulSoup(page2.content, 'html.parser')
                    html2 = list(soup2.children)[2]
                    reviewList2 = soup2.findAll("div", {"class": "review"})

                    for i in range(len(reviewList2)):
                        star = reviewList2[i].find("div", {"class": "metascore_w"})
                        self.starList.append(star.text)
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
            soup1 = BeautifulSoup(page1.content, 'html.parser')
            html1 = list(soup1.children)[2]

            reviewList1 = soup1.findAll("li", {"class": "critic_review"})

            for i in range(len(reviewList1)):
                star = reviewList1[i].find("div", {"class": "metascore_w"})
                self.starList.append(star.text)
                content = reviewList1[i].find("div", {"class": "review_body"})
                self.contentList.append(content.text)

            userReviews = soup.find("a", string="User Reviews")
            userReviews = userReviews['href']
            userReviews = str(userReviews)

            url2 = "https://www.metacritic.com" + userReviews
            page2 = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0'})
            soup2 = BeautifulSoup(page2.content, 'html.parser')
            html2 = list(soup2.children)[2]

            pages = soup2.find("ul", {"class": "pages"})

            reviewList2 = soup2.findAll("li", {"class": "user_review"})

            for j in range(len(reviewList2)):
                star = reviewList2[j].find("div", {"class": "metascore_w"})
                self.starList.append(star.text)
                content = reviewList2[j].find("div", {"class": "review_body"})
                self.contentList.append(content.text)

            if pages:

                nextpage = soup2.find("a", {"rel": "next"})

                while nextpage:
                    nextpage = nextpage['href']
                    url3 = "https://www.metacritic.com" + nextpage
                    page3 = requests.get(url3, headers={'User-Agent': 'Mozilla/5.0'})
                    soup3 = BeautifulSoup(page3.content, 'html.parser')
                    html3 = list(soup3.children)[2]

                    reviewList3 = soup3.findAll("li", {"class": "user_review"})

                    for h in range(len(reviewList3)):
                        star = reviewList3[h].find("div", {"class": "metascore_w"})
                        self.starList.append(star.text)
                        content = reviewList3[h].find("div", {"class": "review_body"})
                        self.contentList.append(content.text)

                    nextpage = soup3.find("a", {"rel": "next"})
        print(self.contentList[0])

    ''' def entrenador_archivos(self):


         print("Ejecutando el entrenador...")
         nltk.download('stopwords')
         stemmer = PorterStemmer()

         valoraciones = load_files(ruta)
         print(len(valoraciones.data))
         X, y = valoraciones.data, valoraciones.target

         self.nombre_etiquetas = valoraciones.target_names
         documentos = []
         '''
    ''' 
                Aqui hacemos el procesamiento de texto usando expresiones regulares.
                Para ello vamos limpiando los archivos poco a poco, empezando por quitar los carácteres especiales (".", ","...),
                después los carácteres que están solos ("a", "y",...),...

                La función re.sub() cambia lo que detecte con la expresion regular por otro texto.
                En este caso lo cambia por nada, es decir, lo elimina
            '''


''' for sen in range(0, len(X)):
# Elimina: carácteres especiales
documento = re.sub(r'\W', ' ', str(X[sen]))

# Elimina: carácteres solos
# remove all single characters
documento = re.sub(r'\s+[a-zA-Z]\s+', ' ', documento)

# Elimina: números
documento = re.sub(r'\d',' ', documento)

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

self.stopword = str(self.ventanaEntrenamiento.comboBox_stopwords.currentText())

'''
'''
                Con TFidVectorizer indicamos la importancia que tiene cada una de las palabras en el documento.

                Para que el programa entienda el texto, hay que cambiar cada una de las palabras a su coincidente numero 
                binario.

                "Max_features" es muy importante, ya que limita a 1500 el numero de palabras que se vayan a usar para el
                clasificador, cogiendo las que mas frecuencia tengan.
            '''

'''    self.vectorizador = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words(self.stopword))

# Almacenamos las palabras en su respectivo formato numerico en X
X = self.vectorizador.fit_transform(documentos).toarray()

X_entrenamiento, X_test, y_entrenamiento, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

self.elegir_algoritmo()

self.algoritmo.fit(X_entrenamiento, y_entrenamiento)
y_pred = self.algoritmo.predict(X_test)
matriz_confusion = confusion_matrix(y_test, y_pred)

figura = plt.figure()
ax = figura.add_subplot(111)

cmap = plt.get_cmap('Blues')
cax = ax.matshow(matriz_confusion, interpolation='nearest', cmap=cmap)
figura.colorbar(cax)

etiquetas = np.arange(len(self.nombre_etiquetas))
plt.xticks(etiquetas, self.nombre_etiquetas, rotation=45)
plt.yticks(etiquetas, self.nombre_etiquetas)

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

label = QLabel(self.ventanaEntrenamiento)
pixmap = QPixmap('./Resources/UIElements/Matriz.png')
label.setPixmap(pixmap)
label.setAlignment(Qt.AlignCenter)
label.show()
self.ventanaEntrenamiento.lay.addWidget(label)

true_positive = matriz_confusion[0][0]
false_positive = matriz_confusion[0][1]
false_negative = matriz_confusion[1][0]
true_negative = matriz_confusion[1][1]

print(matriz_confusion)
print(classification_report(y_test, y_pred))
self.precision = accuracy_score(y_test, y_pred)

self.setVariables_visibles()

print('True positive = ', true_positive)
print('False positive = ', false_positive)
print('False negative = ', false_negative)
print('True negative = ', true_negative)
def choose_algorithm(self):
self.algorithm_name = str(self.view.comboBox_algoritmos.currentText())

if self.algorithm_name == 'Random Forest':
self.algorithm = RandomForestClassifier(n_estimators=1000, random_state=0)

elif self.algorithm_name == 'Naive Bayes':
self.algorithm = GaussianNB()'''
