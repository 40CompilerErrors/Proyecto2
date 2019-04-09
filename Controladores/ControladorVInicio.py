from Controladores import ControladorVClasificador
from Controladores import ControladorVEntrenamiento
from Ventanas import VentanaClasificador
from Ventanas import VentanaEntrenamiento


class ControladorVInicio_class:

    def __init__(self):
        print("Controlador inicial en ejecución...")

    def asignarVentana (self, ventanaInicio):
        self.ventanaInicio=ventanaInicio

    def abrir_clasificador(self):
        ctrl = ControladorVClasificador.ControladorVClasificador_class()
        ventanaClasificador = VentanaClasificador.VentanaClasificador_class(ctrl)
        ctrl.asignarVentana(ventanaClasificador)
        ctrl.obtener_modelos()
        ventanaClasificador.show()

    def abrir_entrenamiento(self):
        ctrl = ControladorVEntrenamiento.ControladorVEntrenamiento_class()
        ventanaEntrenamiento = VentanaEntrenamiento.VentanaEntrenamiento_class(ctrl)
        ctrl.asignarVentana(ventanaEntrenamiento)
        ventanaEntrenamiento.show()