import os
import time

from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from decimal import Decimal
import pickle
import shutil
from nltk.stem.porter import *
from textblob import TextBlob


class ControladorVClasificador_class:

    def __init__(self):
        print("Controlador principal inicializado...")
        self.ruta = ''
        self.lista_archivos = []
        self.seleccionados = []
        self.lista_modelos = []
        self.datos_analisis = []
        self.datos_subjetividad = []
        self.ruta_salida = ''


    def asignarVentana (self, ventanaClasificador):
        self.ventanaClasificador=ventanaClasificador

    def obtener_salida(self):
        self.ruta_salida = QFileDialog.getExistingDirectory()
        print(f'Ruta de salida = {self.ruta_salida}')

    def abrir_archivo(self):
        try:
            self.ventanaClasificador.label_5.setText('Datos seleccionados')
            self.ventanaClasificador.datos_seleccionados.setRowCount(0)
            j = 0
            #Limpia la lista de archivos al elegir una ruta nueva
            for i in self.lista_archivos:
                print(f"Eliminando {i}")
                self.lista_archivos.pop(j)
                j = j+1

            #limpia la tabla que no se añadan a la tabla los datos de una ruta nueva.
            while self.ventanaClasificador.lista_archivos_2.rowCount() > 0:
                    self.ventanaClasificador.lista_archivos_2.removeRow(0)

            self.ruta = QFileDialog.getExistingDirectory()
            if not self.ruta:
                print("El usuario no ha elegido ninguna ruta.")
            else:
                print(f"Ruta: {self.ruta}")
                self.ventanaClasificador.label_ruta_2.setText(self.ruta)
                print(f"Lista de los archivos de la ruta: {os.listdir(self.ruta)}")
                contador = 0
                for archivo in os.listdir(self.ruta):
                    nombre_archivo = f"{archivo}"
                    if(nombre_archivo.endswith(".txt")):
                        rowPosition = self.ventanaClasificador.lista_archivos_2.rowCount()
                        self.ventanaClasificador.lista_archivos_2.insertRow(rowPosition)
                        self.lista_archivos.append(archivo)
                        # Obtiene la ruta entera del archivo que se esta metiendo en la tabla
                        file_status_array = os.stat(f"{self.ruta}/{archivo}")
                        # Obtenemos el tamaño del archivo en cuestion
                        tamaño_archivo = file_status_array.st_size

                        fecha_mod = file_status_array.st_mtime
                        fecha_final = time.ctime(fecha_mod)

                        self.ventanaClasificador.lista_archivos_2.setItem(rowPosition, 0, QTableWidgetItem(f"{contador}"))
                        self.ventanaClasificador.lista_archivos_2.setItem(rowPosition, 1, QTableWidgetItem(nombre_archivo))
                        self.ventanaClasificador.lista_archivos_2.setItem(rowPosition, 2, QTableWidgetItem(f"{tamaño_archivo} bytes"))
                        self.ventanaClasificador.lista_archivos_2.setItem(rowPosition, 3, QTableWidgetItem(f"{fecha_final}"))

                        contador = contador + 1

        except ValueError:
            print('¡¡Fallo al abrir el explorador de archivos!!')

    def anadir_datos(self):
        self.ventanaClasificador.boton_clasificador.setText("Ejecutar Clasificador")
        print("Entrando en añadir datos...")
        try:
            contador = 0
            archivos_seleccionados = self.ventanaClasificador.lista_archivos_2.selectionModel().selectedRows()
            for index in sorted(archivos_seleccionados):
                rowPosition = self.ventanaClasificador.datos_seleccionados.rowCount()

                #sacamos la posicion del archivo seleccionado de la QTableWidget
                posicion_lista = index.row() - contador
                archivo = self.lista_archivos[posicion_lista]
                print(f"Archivo en posicion {posicion_lista}: {archivo}")
                self.seleccionados.append(archivo)

                # Obtiene la ruta entera del archivo que se esta metiendo en la tabla
                file_status_array = os.stat(f"{self.ruta}/{archivo}")

                # Obtenemos el tamaño del archivo en cuestion
                tamaño_archivo = file_status_array.st_size
                fecha_mod = file_status_array.st_mtime
                fecha_final = time.ctime(fecha_mod)

                self.ventanaClasificador.datos_seleccionados.insertRow(rowPosition)
                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))
                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 1, QTableWidgetItem(archivo))
                #self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 2, QTableWidgetItem(f"{tamaño_archivo} bytes"))
                #self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 3, QTableWidgetItem(f"{fecha_final}"))

                self.ventanaClasificador.lista_archivos_2.removeRow(posicion_lista)
                self.lista_archivos.pop(posicion_lista)
                print(f"Eliminado {archivo}")
                contador = contador + 1
        except ValueError:
            print('Fallo al añadir los datos a la tabla de "Datos seleccionados"')

    def anadir_todos(self):
        self.ventanaClasificador.boton_clasificador.setText("Ejecutar Clasificador")
        print("Has pulsado el boton de Añadir Todos los archivos.")
        try:
            tamaño_lista = len(self.lista_archivos)
            for i in range(0,tamaño_lista):
                archivo = self.lista_archivos[i]
                rowPosition = self.ventanaClasificador.datos_seleccionados.rowCount()
                self.seleccionados.append(archivo)

                # Obtiene la ruta entera del archivo que se esta metiendo en la tabla
                file_status_array = os.stat(f"{self.ruta}/{archivo}")

                # Obtenemos el tamaño del archivo en cuestion
                tamaño_archivo = file_status_array.st_size
                fecha_mod = file_status_array.st_mtime
                fecha_final = time.ctime(fecha_mod)

                self.ventanaClasificador.datos_seleccionados.insertRow(rowPosition)
                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))
                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 1, QTableWidgetItem(archivo))
                #self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 2, QTableWidgetItem(f"{tamaño_archivo} bytes"))
                #self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 3, QTableWidgetItem(f"{fecha_final}"))
                self.ventanaClasificador.lista_archivos_2.removeRow(0)

            self.lista_archivos.clear()

        except ValueError:
            print('Fallo al añadir los datos a la tabla de "Datos seleccionados"')

    def obtener_modelos(self):
        for modelo in os.listdir('./Modelos'):
            self.lista_modelos.append(modelo)
        self.ventanaClasificador.comboBox_modelos.addItems(self.lista_modelos)

    def ejecutar_clasificador(self):
        if not self.ruta:
            self.ventanaClasificador.label.setText("No ha seleccionado ninguna carpeta, porfavor "
                                                                "seleccione alguna carpeta.")
        elif not self.lista_modelos:
            self.ventanaClasificador.boton_clasificador.setText("La lista de modelos esta vacía. porfavor cree algún "
                                                                "modelo")
        elif not self.seleccionados:
            self.ventanaClasificador.boton_clasificador.setText("No ha seleccionado ningun archivo de la lista, "
                                                                "porfavor seleccione algun archivo para clasificar")
        else:
            self.ventanaClasificador.boton_clasificador.setText("Ejecutar clasificador")
            print("Comienza la clasificación...")
            cont = 0
            con = 0
            stemmer = PorterStemmer()
            apoyo = []
            datos_archivos = []
            for i in self.seleccionados:

                archivo = f'{self.ruta}/{i}'
                with open(archivo, 'r', encoding='utf-8') as myfile:
                    data = myfile.read().replace('\n', '')
                    '''test = TextBlob(data)
                    if round(test.sentiment.polarity,2) > 0.3 :
                        self.datos_analisis.append("Positivo")
                    elif round(test.sentiment.polarity, 2) < -0.3:
                        self.datos_analisis.append("Negativo")
                    else:
                        self.datos_analisis.append("Neutral")

                    self.datos_subjetividad.append(str(round(test.sentiment.subjectivity,3)))'''

                    datos_archivos.append(data)
            ''' 
                Aqui hacemos el procesamiento de texto usando expresiones regulares.
                Para ello vamos limpiando los archivos poco a poco, empezando por quitar los carácteres especiales (".", ","...),
                después los carácteres que están solos ("a", "y",...),...

                La función re.sub() cambia lo que detecte con la expresion regular por otro texto.
                En este caso lo cambia por nada, es decir, lo elimina
            '''
            documentos = []
            print("Comienza el pre-procesado")
            for sen in range(0, len(datos_archivos)):
                # Elimina: carácteres especiales
                documento = re.sub(r'\W', ' ', str(datos_archivos[sen]))
                '''
                # Elimina: números
                documento = re.sub(r'\d',' ', documento)'''

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



            nombre_modelo = self.ventanaClasificador.comboBox_modelos.currentText()
            with open(f'./Modelos/{nombre_modelo}', 'rb') as training_model:
                model = pickle.load(training_model)
                diccionarioAntiguo = pickle.load(training_model)
                nombres_etiquetas = pickle.load(training_model)

            X = diccionarioAntiguo.transform(documentos)

            prediccion = model.predict(X)
            print("Prediccion hecha!")

            for y in prediccion:
                if y not in apoyo:
                    apoyo.append(y)
            for i in nombres_etiquetas:
                if not os.path.exists(f'{self.ruta_salida}/{i}'):
                    os.makedirs(f'{self.ruta_salida}/{i}')

            rootdir = os.path.dirname(os.path.abspath(__file__))
            dir = os.path.join(os.path.dirname(rootdir), self.ruta)
            dir1 = os.path.join(os.path.dirname(rootdir), self.ruta_salida)
            self.ventanaClasificador.datos_seleccionados.setRowCount(0)
            self.ventanaClasificador.label_5.setText('Resultados de la clasificación')
            print(os.path.join(dir, str(self.seleccionados[cont])))
            for i in prediccion:
                with open(os.path.join(dir, str(self.seleccionados[cont])), 'r') as archivo:
                    data = archivo.read().replace('\n', '')
                    test = TextBlob(data)
                    self.datos_analisis.append(round(test.sentiment.polarity, 4))

                rowPosition = self.ventanaClasificador.datos_seleccionados.rowCount()
                self.ventanaClasificador.datos_seleccionados.insertRow(rowPosition)

                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 0, QTableWidgetItem(f"{rowPosition}"))

                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 1,
                                                                    QTableWidgetItem(self.seleccionados[cont]))

                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 2,
                                                                    QTableWidgetItem(nombres_etiquetas[i]))

                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 3,
                                                                    QTableWidgetItem(str(round(test.sentiment.polarity, 3))))

                self.ventanaClasificador.datos_seleccionados.setItem(rowPosition, 4,
                                                                    QTableWidgetItem(str(round(test.sentiment.subjectivity, 3))))

                shutil.copyfile(os.path.join(dir, str(self.seleccionados[cont])),
                                os.path.join(os.path.join(dir1, nombres_etiquetas[i]), str(self.seleccionados[cont])))
                cont = cont + 1
            print("Archivos guardados.")

            self.ventanaClasificador.label_finalizado.setVisible(True)
