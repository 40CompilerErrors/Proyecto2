import os
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget,QTableWidget,QGridLayout,QTableWidgetItem,QFileDialog, QLabel

from Ventanas import VentanaAnadirEtiquetas
from Controladores import ControladorVEtiquetas
from Controladores import ControladorVGraficas
from Ventanas import VentanaGraficas

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

class ControladorVEntrenamiento_class:

    def __init__(self):
        print("Controlador entrenamiento inicializado...")

        self.ruta_entrenamiento = ''
        self.opciones = []

        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0

        self.lista_modelos = []
        self.nombre_algoritmo = ''
        self.stopword = ''
        self.algoritmo = ''
        self.y_guardados = ''

        self.vectorizador = ''
        self.nombre_etiquetas = ''


    def asignarVentana(self, ventanaEntrenamiento):
        self.ventanaEntrenamiento = ventanaEntrenamiento

    #Metodo empezado pero nunca acabado
    '''def abrir_VEtiquetas(self):
        ctrl = ControladorVEtiquetas.ControladorVEtiquetas_class()
        ventanaAnadirEtiquetas = VentanaAnadirEtiquetas.VentanaAnadirEtiquetas_class(ctrl)
        ctrl.asignarVentana(ventanaAnadirEtiquetas)
        ventanaAnadirEtiquetas.show()'''

    def abrir_VGraficas(self):
        ctrl = ControladorVGraficas.ControladorVGraficas_class()
        ventanaGraficas = VentanaGraficas.VentanaGraficas_class(ctrl)
        ctrl.asignarVentana(ventanaGraficas)
        ventanaGraficas.show()

    def refrescar(self):
        opciones = self.opciones
        self.ventanaEntrenamiento.opciones1.clear()
        self.ventanaEntrenamiento.opciones1.addItems(opciones)
        self.ventanaEntrenamiento.opciones2.clear()
        self.ventanaEntrenamiento.opciones2.addItems(opciones)
        self.ventanaEntrenamiento.opciones3.clear()
        self.ventanaEntrenamiento.opciones3.addItems(opciones)

    def obtener_ruta(self):
        subdirectorios = []
        rutas = []
        ruta = QFileDialog.getExistingDirectory()
        contador = 1
        self.ruta_entrenamiento = ruta

        if not ruta:
            print("El usuario no ha elegido ninguna ruta.")
        else:
            for carpeta in os.listdir(ruta):
                subdirectorios.append(carpeta)
                self.opciones.append(carpeta)
                r = f"{ruta}/{carpeta}"
                self.ventanaEntrenamiento.lista_Rutas.addItem(r)
                for carpeta in subdirectorios:
                    rutaTotal = f"{ruta}/{carpeta}"


        self.ventanaEntrenamiento.opciones1.addItems(self.opciones)
        self.ventanaEntrenamiento.opciones2.addItems(self.opciones)
        self.ventanaEntrenamiento.opciones3.addItems(self.opciones)

        self.ventanaEntrenamiento.boton_clasificador.setText("Ejecutar Clasificador")
        for i in self.opciones:
            tab = QWidget()
            lay = QGridLayout(tab)
            self.ventanaEntrenamiento.tabWidget_3.addTab(tab, i)
            tabla = QTableWidget()
            tabla.setRowCount(1)
            tabla.setColumnCount(4)
            tabla.setHorizontalHeaderLabels(["ID","Nombre","Tamaño","Última modificación"])
            lay.addWidget(tabla)
            for archivo in os.listdir(rutaTotal):
                nombre_archivo = f"{archivo}"
                nombre_lista = f"lista_ruta_{contador+1}"
                if (nombre_archivo.endswith(".txt")):
                    rowPosition = tabla.rowCount()
                    tabla.insertRow(rowPosition)
                    # Obtiene la ruta entera del archivo que se esta metiendo en la tabla
                    file_status_array = os.stat(f"{rutaTotal}/{archivo}")
                    # Obtenemos el tamaño del archivo en cuestion
                    tamaño_archivo = file_status_array.st_size
                    fecha_mod = file_status_array.st_mtime
                    fecha_final = time.ctime(fecha_mod)
                    tabla.setItem(rowPosition, 0, QTableWidgetItem(f"{contador}"))
                    tabla.setItem(rowPosition, 1, QTableWidgetItem(nombre_archivo))
                    tabla.setItem(rowPosition, 2, QTableWidgetItem(f"{tamaño_archivo} bytes"))
                    tabla.setItem(rowPosition, 3, QTableWidgetItem(f"{fecha_final}"))
                    contador = contador + 1
    def entrenador_archivos(self):

        if not self.ruta_entrenamiento:
            self.ventanaEntrenamiento.label_advertencias.setText("No introdujo una ruta, "
                                                                 "introduzca un ruta porfavor")
            self.ventanaEntrenamiento.label_advertencias.setVisible(True)
        else:
            self.ventanaEntrenamiento.label_advertencias.setVisible(False)
            print("Ejecutando el entrenador...")
            nltk.download('stopwords')
            stemmer = PorterStemmer()
            ruta = self.ruta_entrenamiento

            valoraciones = load_files(ruta)
            X, y = valoraciones.data, valoraciones.target

            self.nombre_etiquetas = valoraciones.target_names

            documentos = []
            ''' 
                Aqui hacemos el procesamiento de texto usando expresiones regulares.
                Para ello vamos limpiando los archivos poco a poco, empezando por quitar los carácteres especiales (".", ","...),
                después los carácteres que están solos ("a", "y",...),...

                La función re.sub() cambia lo que detecte con la expresion regular por otro texto.
                En este caso lo cambia por nada, es decir, lo elimina
            '''
            for sen in range(0, len(X)):
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
                Con TFidVectorizer indicamos la importancia que tiene cada una de las palabras en el documento.

                Para que el programa entienda el texto, hay que cambiar cada una de las palabras a su coincidente numero 
                binario.

                "Max_features" es muy importante, ya que limita a 1500 el numero de palabras que se vayan a usar para el
                clasificador, cogiendo las que mas frecuencia tengan.
            '''

            self.vectorizador = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words(self.stopword))

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
            figura.savefig('./Imagenes/Matrices_Confusion/Matriz.png')
            print("Imagen guardada")

            label = QLabel(self.ventanaEntrenamiento)
            pixmap = QPixmap('./Imagenes/Matrices_Confusion/Matriz.png')
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



    def guardar_modelo(self):
        nombre_modelo = self.ventanaEntrenamiento.textField_nombreModelo.toPlainText()
        if not nombre_modelo:
            self.ventanaEntrenamiento.label_advertencias.setText("[ADVERTENCIA] No se ha introducido nombre al modelo.\n No se puede efectuar el entrenamiento.")
            self.ventanaEntrenamiento.label_advertencias.setVisible(True)
        else:
            # Aqui guardamos el Modelo en formato pickle
            with open(f'./Modelos/{nombre_modelo}', 'wb') as modelo_completo:
                pickle.dump(self.algoritmo, modelo_completo)
                pickle.dump(self.vectorizador, modelo_completo)
                pickle.dump(self.nombre_etiquetas, modelo_completo)

            self.ventanaEntrenamiento.label_guardarModelo.setVisible(True)


    def elegir_algoritmo(self):
        self.nombre_algoritmo = str(self.ventanaEntrenamiento.comboBox_algoritmos.currentText())

        if self.nombre_algoritmo == 'Random Forest':
            self.algoritmo = RandomForestClassifier(n_estimators=1000, random_state=0)

        elif self.nombre_algoritmo == 'Naive Bayes':
            self.algoritmo = GaussianNB()
        else:
            print("No se ha seleccionado ningun algoritmo.")

    def setVariables_visibles(self):
        self.ventanaEntrenamiento.label_precision.setText(f"La precision del algoritmo es de un {self.precision*100}%")
        self.ventanaEntrenamiento.label_precision.setVisible(True)
        self.ventanaEntrenamiento.label_exito.setVisible(True)
        self.ventanaEntrenamiento.boton_guardarModelo.setVisible(True)
