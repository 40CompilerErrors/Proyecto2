from Controllers import AdminController as AC
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from Views import AdminMenu as AM


class TrainOutputWindow(QMainWindow):

    def __init__(self,controller):
        super(TrainOutputWindow, self).__init__()

        self.controller = controller
        loadUi('./Resources/UI/OutputWindowEntrenamientoWeb.ui', self)

        self.setWindowTitle('VentanaEntrenamiento')

        # self.initiateVariables()
        self.buttonActions()
        self.label_guardarModelo_.setVisible(False)

    def buttonActions(self):
        self.boton_guardarModelo_.clicked.connect(self.controller.guardar_modelo)
        self.backButton.clicked.connect(self.controller.goBack)