from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from Controllers import ClassifyController as CC



class ClassifyMenu(QMainWindow):

    # metodo para iniciar la clase VentanaClasificador
    def __init__(self):
        super(ClassifyMenu, self).__init__()

        #creamos un elemento controlador para poder llamar a las funciones de este.
        self.controller = CC.ClassifyController(self)

        loadUi('./Resources/UI/VentanaClasificador.ui', self)

        self.setWindowTitle('Ventana Clasificador')
        self.label_finalizado.setVisible(False)
        self.controller.obtener_modelos()
        self.acciones_ctrl()


    def acciones_ctrl(self):
        self.boton_ruta_2.clicked.connect(self.controller.abrir_archivo)
        self.boton_anadir_todos.clicked.connect(self.controller.anadir_todos)
        #self.anadir_archivo_2.clicked.connect(self.controller.anadir_datos)
        self.boton_clasificador.clicked.connect(self.controller.ejecutar_clasificador)
        self.boton_guardar.clicked.connect(self.controller.obtener_salida)
        self.boton_clasificador.setShortcut("ENTER")
