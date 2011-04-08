import ui
import os
import sys
import glob
from PyQt4 import QtGui, QtCore

class VentanaPrincipal(QtGui.QMainWindow, ui.Ui_MainWindow):

    def __init__(self):
        self._iniciar_interfaz()

        self._cargar_lista_de_ejemplos()

        # Senales
        self.connect(self.ui.ejecutar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_boton_ejecutar)
        self.connect(self.ui.guardar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_boton_guardar)
        self.connect(self.ui.lista, QtCore.SIGNAL("itemSelectionChanged()"), self.cuando_cambia_seleccion)

    def _cargar_lista_de_ejemplos(self):
        todos_los_archivos = glob.glob("ejemplos/*.py")
        nombres = [x.replace('.py', '').replace('ejemplos/','') for x in todos_los_archivos]

        for n in nombres:
            self.ui.lista.addItem(n)

    def _iniciar_interfaz(self):
        QtGui.QMainWindow.__init__(self)
        ui.Ui_MainWindow.__init__(self)
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

    def cuando_pulsa_boton_ejecutar(self):
        nombre_ejemplo = str(self._obtener_item_actual() + '.py')

        pid = os.fork()

        if pid == 0:
            execfile(nombre_ejemplo)

    def cuando_pulsa_boton_guardar(self):
        print self._obtener_item_actual()

    def cuando_cambia_seleccion(self):
        nombre = self._obtener_item_actual()
        self._mostrar_codigo_del_ejemplo(nombre)
        self._mostrar_imagen_del_ejemplo(nombre)

    def _mostrar_imagen_del_ejemplo(self, nombre):
        escena = QtGui.QGraphicsScene()
        self.ui.imagen.setScene(escena)
        pixmap = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('ejemplos/' + nombre + '.png'))
        escena.addItem(pixmap);

    def _mostrar_codigo_del_ejemplo(self, nombre):
        archivo = open('ejemplos/' + nombre + '.py', 'rt')
        contenido = archivo.read()
        archivo.close()
        self.ui.codigo.document().setPlainText(contenido)

    def _obtener_item_actual(self):
        return self.ui.lista.currentItem().text()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec_())

