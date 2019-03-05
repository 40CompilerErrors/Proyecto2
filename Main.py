from Controladores import ControladorVInicio
from Ventanas import VentanaInicio
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    #iniciamos la aplicación
    app = QApplication(sys.argv)

    # iniciamos el controlador
    ctrl = ControladorVInicio.ControladorVInicio_class()

    #creamos la ventana principal de la aplicacion
    ventanaInicio = VentanaInicio.VentanaInicio_class(ctrl)

    #asociamos el controlador a la ventana
    ctrl.asignarVentana(ventanaInicio)

    #mostramos la ventana
    ventanaInicio.show()

    sys.exit(app.exec_())

