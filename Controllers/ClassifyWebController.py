import os
import csv
from PyQt5.QtWidgets import QFileDialog
import pickle
from nltk.corpus import stopwords
import pandas as pd
from nltk.stem.porter import *
from PyQt5.QtWidgets import QTableWidgetItem
import re

from textblob import TextBlob

from Model.Scrappers import MetacriticScrapper as MS, AmazonScrapper as AS, SteamScrapper as SS, YelpScrapper as YS

class ClassifyWebController:

    def __init__(self, view):
        self.view = view
        self.linkList = []
        self.modelsList = []
        self.reviewList = []
        self.support = []
        self.contentList = []
        self.analysis_data = []
        self.ruta_salida = ''

    def validate(self):
        if 'https://www.metacritic.com' in self.view.url_line.text() and self.view.pages_combo.currentText() == 'Metacritic':
            self.addURL()
            self.view.label_2.setText('Inserte las URLs: ')
        elif 'store.steampowered.com' in self.view.url_line.text() and self.view.pages_combo.currentText() == 'Steam':
            self.addURL()
            self.view.label_2.setText('Inserte las URLs: ')
        elif 'https://www.amazon.com' in self.view.url_line.text() and self.view.pages_combo.currentText() == 'Amazon':
            self.addURL()
            self.view.label_2.setText('Inserte las URLs: ')
        elif 'https://www.yelp.' in self.view.url_line.text() and self.view.pages_combo.currentText() == 'Yelp':
            self.addURL()
            self.view.label_2.setText('Inserte las URLs: ')
        else:
            self.view.label_2.setText('No introdujo correctamente la URL. Porfavor introduzca de nuevo la URL')

    def addURL(self):
        link = self.view.url_line.text()
        self.linkList.append(link)
        rowPosition = self.view.url_table.rowCount()
        self.view.url_table.insertRow(rowPosition)
        self.view.url_table.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))
        self.view.url_table.setItem(rowPosition, 1, QTableWidgetItem(str(link)))
        self.view.url_line.setText("")

    def obtainModels(self):
        for model in os.listdir('./Resources/Models'):
            self.modelsList.append(model)
        self.view.comboBox_modelos.addItems(self.modelsList)

    def obtainRoute(self):
        self.ruta_salida = QFileDialog.getExistingDirectory()

    def scrapLinks(self):
        metacriticScrapper = MS.MetacriticScrapper()
        steamScrapper = SS.SteamScrapper()
        yelpScrapper = YS.YelScrapper()
        amazonScrapper = AS.AmazonScrapper()
        if not self.linkList:
            self.view.label_3.setVisible(True)
        else:
            self.view.label_3.setVisible(False)
            for url in self.linkList:
                print("Scrapping link: " + url)
                url_stars, url_reviews = [], []
                if 'metacritic.com' in url:
                    print("Detected as Metacritic URL")
                    url_stars, url_reviews = metacriticScrapper.scrapURL(url)
                elif 'store.steampowered.com' in url:
                    print("Detected as Steam URL")
                    url_stars, url_reviews = steamScrapper.scrapURL(url)
                elif 'amazon.com' in url:
                    print("Detected as Amazon URL")
                    url_stars, url_reviews = amazonScrapper.scrapURL(url)
                elif 'yelp.com' in url:
                    print("Detected as Yelp URL")
                    url_stars, url_reviews = yelpScrapper.scrapURL(url)
                else:
                    print("Detected as invalid link")
                print("Finished scrapping URL")
                self.contentList += url_reviews

    def ejecutar_clasificador(self):

        if not self.modelsList:
            self.view.boton_clasificador.setText("La lista de modelos esta vacía. porfavor cree algún "
                                                                "modelo")
        elif not self.ruta_salida:
            self.view.label_6.setText('Porfavor elija una ruta para guardar las reviews')
        else:
            self.view.label_6.setText('Elegir la ruta donde se guardarán los archivos clasificados:')
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

            rootdir = os.path.dirname(os.path.abspath(__file__))
            dir1 = os.path.join(os.path.dirname(rootdir), self.ruta_salida)
            self.view.datos_seleccionados.setRowCount(0)
            self.view.label_5.setText('Resultados de la clasificación')

            elementLists = []
            for i in prediccion:
                elementList = []
                data = self.contentList[cont].replace('\n', '')
                test = TextBlob(data)
                self.analysis_data.append(round(test.sentiment.polarity, 4))

                rowPosition = self.view.datos_seleccionados.rowCount()
                self.view.datos_seleccionados.insertRow(rowPosition)

                self.view.datos_seleccionados.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))

                self.view.datos_seleccionados.setItem(rowPosition, 1,
                                                                    QTableWidgetItem(self.contentList[cont]))

                self.view.datos_seleccionados.setItem(rowPosition, 2,
                                                                    QTableWidgetItem(str(labelsName[i])))

                self.view.datos_seleccionados.setItem(rowPosition, 3,
                                                                    QTableWidgetItem(str(round(test.sentiment.polarity, 3))))

                self.view.datos_seleccionados.setItem(rowPosition, 4,
                                                                    QTableWidgetItem(str(round(test.sentiment.subjectivity, 3))))


                print('llegoantes')
                elementLists.append([str(labelsName[i]), str(round(test.sentiment.polarity, 3)),
                                     str(round(test.sentiment.subjectivity, 3)),self.contentList[cont]])
                print('llegodespues')
                cont = cont + 1
            print('llego3')
            headers = ["Label", "Polarity", "Subjectivity", "Body"]
            print('llego4')
            dataframe = pd.DataFrame(elementLists,columns=headers)
            print('llego5')
            print(dataframe)

            if not self.ruta_salida == '':
                dataframe.to_csv(os.path.join(dir1,"results.csv"), encoding='utf-8', index=False)


            print("Archivos guardados.")
            c = 0

            self.view.label_finalizado.setVisible(True)
