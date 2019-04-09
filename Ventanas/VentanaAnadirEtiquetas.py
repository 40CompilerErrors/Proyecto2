from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class VentanaAnadirEtiquetas_class(QDialog):

    # metodo para iniciar la clase VentanaAñadirEtiqueta
    def __init__(self, controlador):
        super(VentanaAnadirEtiquetas_class, self).__init__()
        self.controlador = controlador

        loadUi('./User_Interfaces/VentanaAnadirEtiqueta.ui', self)
        self.setWindowTitle('Añadir Etiqueta')
        self.boton_Anadir.clicked.connect(controlador.anadir_etiquetas)
        self.boton_Volver.clicked.connect(self.close)
        self.label_comprobacion.setVisible(False)