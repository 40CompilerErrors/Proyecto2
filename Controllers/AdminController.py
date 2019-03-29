from Views import TrainMenu as TM, TrainWebMenu as TWM
from Controllers import TrainController as TC

class AdminController:

    def __init__(self, view):
        self.view = view

    def openTrainer(self):
        ctrl = TC.TrainController()
        ventanaEntrenamiento = TM.TrainMenu(ctrl)
        ctrl.asignarVentana(ventanaEntrenamiento)
        ventanaEntrenamiento.show()

    def openWebScrapper(self):
        window = TWM.TrainWebMenu()
        window.show()