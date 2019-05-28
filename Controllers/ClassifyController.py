import os
import csv
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
import pickle
import pandas as pd
from nltk.stem.porter import *
from PyQt5.QtWidgets import QTableWidgetItem
import glob
import re
from Views import ClassifyInputWindow as CIW, ClassifyOutputWindow as COW
from Model import Model as MD


from textblob import TextBlob

from Utilities.DB_Driver import DB_Driver
from Utilities.Scrappers import MetacriticScrapper as MS, SteamScrapper as SS, YelpScrapper as YS
from Utilities.Scrappers import AmazonScrapper as AS
from Model import Review as REV


class ClassifyWebController:

    def __init__(self):

        self.linkList = []
        self.modelsList = []
        self.reviewList = []
        self.support = []
        self.contentList = []
        self.analysis_data = []
        self.ruta_salida = ''


        self.metacriticScrapper = MS.MetacriticScrapper()
        self.steamScrapper = SS.SteamScrapper()
        self.yelpScrapper = YS.YelScrapper()
        self.amazonScrapper = AS.AmazonScrapper()

        self.view = CIW.ClassifyInputWindow(self)
        self.showModels()
        self.view.show()
        print(self.view)

    def validate(self):

        if 'https://www.metacritic.com' in self.view.url_line.text() and self.view.pages_combo.currentText() == 'Metacritic':
            if re.search("https://www.metacritic.com/movie/.*", self.view.url_line.text()) or re.search("https://www.metacritic.com/game/.*/.*", self.view.url_line.text()) or re.search("https://www.metacritic.com/tv/.*/.*", self.view.url_line.text()) or re.search("https://www.metacritic.com/music/.*/.*", self.view.url_line.text()):
                self.addURL()
            else:
                self.view.messages.setText('Fallo con la ruta de Metacritic.')
        elif 'store.steampowered.com' in self.view.url_line.text() and self.view.pages_combo.currentText() == 'Steam':
            if re.search("store.steampowered.com/app/.*", self.view.url_line.text()):
                self.addURL()
            else:
                self.view.messages.setText('Fallo con la ruta de Steam.')
        elif 'https://www.amazon.com' in self.view.url_line.text() and self.view.pages_combo.currentText() == 'Amazon':
            if re.search("https://www.amazon.com/.*?/ref", self.view.url_line.text()):
                self.addURL()
            else:
                self.view.messages.setText('Fallo con la ruta de Amazon.')
        elif 'https://www.yelp.' in self.view.url_line.text() and self.view.pages_combo.currentText() == 'Yelp':
            if re.search("yelp.*/biz/.*", self.view.url_line.text()):
                self.addURL()
            else:
                self.view.messages.setText('Fallo con la ruta de Yelp.')
        else:
            self.view.messages.setText('La ruta no es válida. Por favor inserte una ruta válida.')

    def addURL(self):
        link = self.view.url_line.text()
        self.linkList.append(link)
        self.view.messages.setText('Scrapping...')
        review_number = self.scrapLink(link)
        

        # Add the current link to the table
        rowPosition = self.view.url_table.rowCount()
        self.view.url_table.insertRow(rowPosition)
        item = QTableWidgetItem(f"{rowPosition}")
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item2 = QTableWidgetItem(str(review_number))
        item2.setFlags(QtCore.Qt.ItemIsEnabled)
        item3 = QTableWidgetItem(str(link))
        item3.setFlags(QtCore.Qt.ItemIsEnabled)
        self.view.url_table.setItem(rowPosition, 0, item )
        self.view.url_table.setItem(rowPosition, 1, QTableWidgetItem(str(review_number)))
        self.view.url_table.setItem(rowPosition, 2, QTableWidgetItem(str(link)))
        self.view.url_line.setText("")

    def downloadModels(self):
        # Download from S3
        self.view.messages.setText("Downloading models from remote storage...")

        MD.Model().downloadModels();

        self.modelList = []
        while self.view.comboBox_modelos.count() > 0:
            self.view.comboBox_modelos.removeItem(0)
        self.showModels()
        self.view.messages.setText("Models downloaded successfully!")

    def showModels(self):
        for model in os.listdir('./Resources/Models'):
            self.modelsList.append(model)
        self.view.comboBox_modelos.addItems(self.modelsList)
        #Need to make this work with S3

    def obtainRoute(self):
        self.ruta_salida = QFileDialog.getExistingDirectory()
        self.view.directoryLine.setText(self.ruta_salida)

        #Add saving files here


    def scrapLink(self, url):
        #For some reason it's REALLY not loading
        self.view.messages.setText("Scrapping URL: " + url)
        self.view.update()
        # if not self.linkList:
        #     # self.view.label_3.setVisible(True)
        #     pass
        # else:
            # self.view.label_3.setVisible(False)

        print("Scrapping link: " + url)
        url_stars, url_reviews = [], []
        if 'metacritic.com' in url:
            print("Detected as Metacritic URL")
            url_stars, url_reviews = self.metacriticScrapper.scrapURL(url)
        elif 'store.steampowered.com' in url:
            print("Detected as Steam URL")
            url_stars, url_reviews = self.steamScrapper.scrapURL(url)
        elif 'amazon.com' in url:
            print("Detected as Amazon URL")
            url_stars, url_reviews = self.amazonScrapper.scrapURL(url)
        elif 'yelp.com' in url:
            print("Detected as Yelp URL")
            url_stars, url_reviews = self.yelpScrapper.scrapURL(url)
        else:
            print("Detected as invalid link")
        print("Finished scrapping URL")
        self.contentList += url_reviews
        self.view.messages.setText("Successfully scrapped " + url)
        return len(url_reviews)


    def switch_view(self,new_view):
        self.view.close()
        self.view = new_view(self)
        self.view.show()

    def goBack(self):
        self.linkList = []
        self.modelsList = []
        self.reviewList = []
        self.support = []
        self.contentList = []
        self.analysis_data = []
        self.ruta_salida = ''

        self.switch_view(CIW.ClassifyInputWindow)
        

    def ejecutar_clasificador(self):

        if not self.modelsList:
            self.view.boton_clasificador.setText("La lista de modelos esta vacía. porfavor cree algún modelo")
        else:
            # self.view.label_6.setText('Elegir la ruta donde se guardarán los archivos clasificados:')
            self.view.boton_clasificador.setText("Ejecutar clasificador")
            print("Comienza la clasificación...")
            cont = 0
            con = 0
            stemmer = PorterStemmer()

            documentos = []
            print("Comienza el pre-procesado")
            for sen in range(0, len(self.contentList)):
                # Elimina: carácteres especiales
                documento = re.sub(r'\W', ' ', str(self.contentList[sen]))

                # Elimina: carácteres solos
                documento = re.sub(r'\s+[a-zA-Z]\s+', ' ', documento)

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

            model_name = self.view.comboBox_modelos.currentText()
            with open(f'./Resources/Models/{model_name}', 'rb') as training_model:
                model = pickle.load(training_model)
                diccionarioAntiguo = pickle.load(training_model)
                labelsName = pickle.load(training_model)


            X = diccionarioAntiguo.transform(documentos)

            prediccion = model.predict(X)
            print("Prediccion hecha!")

            for y in prediccion:
                if y not in self.support:
                    self.support.append(y)
            '''for i in labelsName:
                if not os.path.exists(f'{self.ruta_salida}/{i}'):
                    os.makedirs(f'{self.ruta_salida}/{i}')'''


            # self.view.label_5.setText('Resultados de la clasificación')

            self.switch_view(COW.ClassifyOutputWindow)

            self.view.datos_seleccionados.setRowCount(0)

            elementLists = []

            for i in prediccion:
                elementList = []
                data = self.contentList[cont].replace('\n', '')
                test = TextBlob(data)
                self.analysis_data.append(round(test.sentiment.polarity, 4))

                rowPosition = self.view.datos_seleccionados.rowCount()
                self.view.datos_seleccionados.insertRow(rowPosition)

                self.view.datos_seleccionados.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))
                self.view.datos_seleccionados.setItem(rowPosition, 1, QTableWidgetItem(i))
                self.view.datos_seleccionados.setItem(rowPosition, 2, QTableWidgetItem(str(round(test.sentiment.polarity, 3))))
                self.view.datos_seleccionados.setItem(rowPosition, 3, QTableWidgetItem(str(round(test.sentiment.subjectivity, 3))))
                self.view.datos_seleccionados.setItem(rowPosition, 4, QTableWidgetItem(self.contentList[cont]))

                elementLists.append([i, str(round(test.sentiment.polarity, 3)),
                                     str(round(test.sentiment.subjectivity, 3)),self.contentList[cont]])

                cont = cont + 1

            headers = ["Label", "Polarity", "Subjectivity", "Body"]
            self.result_DF = pd.DataFrame(elementLists,columns=headers)
            print(self.result_DF)

    def saveResults(self):
        pass

    def addFromFile(self):
        dir = str(QFileDialog.getExistingDirectory(self.view, "Select Directory"))

        self.contentList = REV.Review().loadCSV(dir)
        review_count = len(self.contentList)

        rowPosition = self.view.url_table.rowCount()
        self.view.url_table.insertRow(rowPosition)
        self.view.url_table.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))
        self.view.url_table.setItem(rowPosition, 1, QTableWidgetItem(str(review_count)))
        self.view.url_table.setItem(rowPosition, 2, QTableWidgetItem(str(file)))


    def removeReviews(self):
        self.view.messages.setText("Removing reviews...")
        self.linkList = []
        self.contentList = []
        while self.view.url_table.rowCount() > 0:
            self.view.url_table.removeRow(0)
        self.view.messages.setText("Removed all reviews")