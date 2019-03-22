from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from Controllers import TrainController as TC


class TrainMenu(QMainWindow):
    # metodo para iniciar la clase VentanaEntrenamiento
    def __init__(self,controlador):
        super(TrainMenu, self).__init__()

        # creamos un elemento controlador para poder llamar a las funciones de este.
        self.controlador = controlador
        self.algoritmos = []
        self.stopwords_lenguaje = []

        loadUi('./Resources/UI/VentanaEntrenamiento.ui', self)

        self.setWindowTitle('Entrenamiento')

        self.acciones_botones()
        self.iniciar_variables()
        self.deshabilitar_opciones()


    def iniciar_variables(self):
        self.stopwords_lenguaje = ['english', 'danish', 'dutch', 'arabic', 'finnish', 'french', 'german', 'hungarian',
                                   'italian', 'kazakh', 'norwegian', 'portuguese', 'romanian', 'russian', 'spanish',
                                   'swedish', 'turkish']
        self.algoritmos = ['Random Forest', 'Naive Bayes']
        for i in self.algoritmos:
            self.comboBox_algoritmos.addItem(i)

        for i in self.stopwords_lenguaje:
            self.comboBox_stopwords.addItem(i)
        self.label_exito.setVisible(False)
        self.label_precision.setVisible(False)
        self.boton_guardarModelo.setVisible(False)
        self.label_guardarModelo.setVisible(False)
        self.label_advertencias.setVisible(False)

    def acciones_botones(self):
        self.boton_refrescar.clicked.connect(self.controlador.refrescar)
        self.boton_rutaPadre.clicked.connect(self.controlador.obtener_ruta)
        self.boton_clasificador.clicked.connect(self.controlador.entrenador_archivos)
        self.boton_guardarModelo.clicked.connect(self.controlador.guardar_modelo)

    def deshabilitar_opciones(self):
        self.opciones1.setEnabled(False)
        self.opciones2.setEnabled(False)
        self.opciones3.setEnabled(False)