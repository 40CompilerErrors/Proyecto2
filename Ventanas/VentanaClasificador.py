from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow


class VentanaClasificador_class(QMainWindow):

    # metodo para iniciar la clase VentanaClasificador
    def __init__(self, controlador):

        '''
            El prefijo 'self' en Python es como el 'this' en Java.
            Se usa especialmente para acceder a los elementos de un nuevo objeto creado
            de la clase VentanaPrincipal().
        '''

        super(VentanaClasificador_class, self).__init__()

        #creamos un elemento controlador para poder llamar a las funciones de este.
        self.controlador = controlador

        loadUi('./User_Interfaces/VentanaClasificador.ui', self)

        self.setWindowTitle('Clasificador')
        self.boton_ruta_2.setShortcut("Ctrl+S")
        self.label_finalizado.setVisible(False)
        self.acciones_ctrl()


    def acciones_ctrl(self):
        self.boton_ruta_2.clicked.connect(self.controlador.abrir_archivo)
        self.boton_anadir_todos.clicked.connect(self.controlador.anadir_todos)
        self.anadir_archivo_2.clicked.connect(self.controlador.anadir_datos)
        self.boton_clasificador.clicked.connect(self.controlador.ejecutar_clasificador)
        self.boton_guardar.clicked.connect(self.controlador.obtener_salida)
        self.boton_clasificador.setShortcut("ENTER")
