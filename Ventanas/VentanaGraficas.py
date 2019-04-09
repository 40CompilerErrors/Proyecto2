from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class VentanaGraficas_class(QDialog):
    # metodo para iniciar la clase VentanaEntrenamiento
    def __init__(self, controlador):
        super(VentanaGraficas_class, self).__init__()

        # creamos un elemento controlador para poder llamar a las funciones de este.
        self.controlador = controlador

        loadUi('./User_Interfaces/VentanaGraficas.ui', self)

        self.setWindowTitle('Graficas')
