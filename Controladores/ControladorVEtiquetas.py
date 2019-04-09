from Controladores import ControladorVEntrenamiento


class ControladorVEtiquetas_class:

    def __init__(self):
        print("Controlador Ventana Etiquetas inicializado...")

    def asignarVentana(self, ventanaAñadirEtiquetas):
        self.ventanaAñadirEtiquetas=ventanaAñadirEtiquetas

    def anadir_etiquetas(self):
        try:
            texto = self.ventanaAñadirEtiquetas.textfield_etiqueta.toPlainText()
            print(texto)
            ControladorVEntrenamiento.opciones.append(texto)
            self.ventanaAñadirEtiquetas.close()
        except ValueError:
            self.ventanaAñadirEtiquetas.label_comprobacion.setVisible(True)

