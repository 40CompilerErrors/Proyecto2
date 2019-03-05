from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class VentanaInicio_class(QMainWindow):
    # metodo para iniciar la clase VentanaInicio
    def __init__(self, controlador):
        super(VentanaInicio_class, self).__init__()

        # creamos un elemento controlador para poder llamar a las funciones de este.
        self.controlador = controlador

        loadUi('./User_Interfaces/VentanaInicio.ui', self)

        self.setWindowTitle('Pantalla Inicio')
        self.boton_clasificador.clicked.connect(controlador.abrir_clasificador)
        self.boton_entrenamiento.clicked.connect(controlador.abrir_entrenamiento)
        self.setFixedSize(700,300)