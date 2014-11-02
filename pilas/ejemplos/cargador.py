# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

from . import ui
import os
import sys
import glob

from PyQt4 import QtGui, QtCore

from . import syntax
import pilas


MENSAJE_PRESENTACION = u"""Bienvenido al cargador de ejemplos.

Selecciona un ejemplo usando el panel de
la izquierda y luego verás el código acá.
"""


class VentanaEjemplos(ui.Ui_Ejemplos):

    def setupUi(self, main):
        self.main = main
        ui.Ui_Ejemplos.setupUi(self, main)

        self._conectar_signals()
        syntax.PythonHighlighter(self.codigo.document())

        self._definir_estado_habilitado(True)
        self._mostrar_image_inicial()
        self._mostrar_codigo_presentacion_inicial()

        self.this_dir = os.path.abspath(os.path.dirname(__file__))
        self.example_dir = os.path.join(self.this_dir, 'ejemplos')
        self._cargar_lista_de_ejemplos()
        pilas.utils.centrar_ventana(self.main)

    def _conectar_signals(self):
        self.ejecutar.connect(self.ejecutar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_boton_ejecutar)
        self.fuente.connect(self.fuente, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_boton_fuente)
        self.guardar.connect(self.guardar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_boton_guardar)
        self.arbol.connect(self.arbol, QtCore.SIGNAL("itemSelectionChanged()"), self.cuando_cambia_seleccion)
        self.arbol.connect(self.arbol, QtCore.SIGNAL("itemActivated(QListWidgetItem *)"), self.cuando_pulsa_boton_ejecutar)

    def _definir_estado_habilitado(self, esta_habilitado):
        "Oculta la barra de progreso y habilita todos los controles."

        widgets = [self.progreso, self.ejecutar, self.guardar, self.arbol, self.fuente, self.codigo, self.imagen]

        self.progreso.setVisible(not esta_habilitado)

        for x in widgets:
            x.setEnabled(esta_habilitado)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return and \
        self.arbol.hasFocus() and \
        self.arbol.currentItem().childCount() == 0:
            self.cuando_pulsa_boton_ejecutar()

        return QtGui.QMainWindow.keyPressEvent(self, event)

    def _cargar_lista_de_ejemplos(self):
        self.ejemplos = {}
        self.arbol.setColumnCount(1)
        self.arbol.setHeaderLabels(["Nombre"])

        directorios = glob.glob(self.example_dir + '/*')

        for directorio in directorios:
            raiz = QtGui.QTreeWidgetItem([os.path.basename(directorio), ""])
            self.arbol.addTopLevelItem(raiz)

            archivos = glob.glob(directorio + '/*.py')
            archivos.sort()

            for archivo in archivos:
                nombre_legible = os.path.basename(archivo).replace(".py", "")
                item = QtGui.QTreeWidgetItem([nombre_legible, archivo])
                raiz.addChild(item)
                self.ejemplos[nombre_legible] = archivo

    def cuando_pulsa_boton_ejecutar(self):
        nombre_ejemplo = self._obtener_item_actual()
        self._ejecutar_ejemplo(nombre_ejemplo)

    def cuando_pulsa_boton_fuente(self):
        font = self.codigo.font()
        font, ok = QtGui.QFontDialog.getFont(font)

        if ok:
            self.codigo.setFont(font)

    def cuando_pulsa_boton_guardar(self):
        nombre = self._obtener_item_actual()
        path = unicode(QtGui.QFileDialog.getSaveFileName(self.main, 'Guardar ejemplo', nombre, "py (*.py)"))
        if path:
            contenido = self._obtener_codigo_del_ejemplo(nombre)

            archivo = open(path, "wt")
            archivo.write(contenido)
            archivo.close()

    def cuando_cambia_seleccion(self):
        ruta = self._obtener_item_actual()

        if ruta:
            self._mostrar_codigo_del_ejemplo(ruta)
            self._mostrar_imagen_del_ejemplo(ruta)

    def _obtener_item_desde_ruta(self, ruta):
        nombres = ruta.split('/')
        categoria = nombres[-2]
        nombre = nombres[-1].replace('.py', '')

        items = self.arbol.findItems(nombre, QtCore.Qt.MatchRecursive)

        if items:
            return items[0]

    def _mostrar_imagen_del_ejemplo(self, ruta):
        escena = QtGui.QGraphicsScene()
        self.imagen.setScene(escena)
        pixmap = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(ruta.replace('.py', '.png')))
        #ancho = self.imagen.width()
        escena.addItem(pixmap)

    def _mostrar_image_inicial(self):
        path = os.path.join(os.path.dirname(__file__), "data/_presentacion")
        self._mostrar_imagen_del_ejemplo(path)

    def _mostrar_codigo_del_ejemplo(self, nombre):
        contenido = self._obtener_codigo_del_ejemplo(nombre)
        self.codigo.document().setPlainText(contenido)

    def _mostrar_codigo_presentacion_inicial(self):
        self.codigo.document().setPlainText(MENSAJE_PRESENTACION)

    def _obtener_codigo_del_ejemplo(self, nombre):
        archivo = open(nombre)
        contenido = archivo.read()
        archivo.close()
        return contenido

    def _obtener_item_actual(self):
        return self.arbol.currentItem().text(1)

    def _ejecutar_ejemplo(self, ruta):
        self.process = QtCore.QProcess(self.main)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.finished.connect(self._cuando_termina_la_ejecucion_del_ejemplo)
        self.process.start(sys.executable, [ruta])

        # Deshabilita todos los controles para que se pueda
        # ejecutar un ejemplo a la vez.
        self._definir_estado_habilitado(False)

    def _cuando_termina_la_ejecucion_del_ejemplo(self, estado, process):
        "Vuelve a permitir que se usen todos los botone de la interfaz."
        salida = str(self.process.readAll())

        if estado:
            QtGui.QMessageBox.critical(self.main, "Error al iniciar ejemplo", "Error: \n" + salida)

        self._definir_estado_habilitado(True)
        self.arbol.setFocus()

def main(parent=None):
    dialog = QtGui.QDialog(parent)
    dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)
    ui = VentanaEjemplos()
    ui.setupUi(dialog)
    dialog.exec_()

if __name__ == "__main__":
    main()
