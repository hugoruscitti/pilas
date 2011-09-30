# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import ui
import os
import sys
import glob

from PyQt4 import QtGui, QtCore

import syntax
import buscador


MENSAJE_PRESENTACION = u"""Bienvenido al cargador de ejemplos.

Selecciona un ejemplo usando el panel de
la izquierda y luego verás el código acá.
"""


class VentanaPrincipal(QtGui.QMainWindow, ui.Ui_MainWindow):

    def __init__(self):
        self._iniciar_interfaz()
        self.this_dir = os.path.abspath(os.path.dirname(__file__))
        self.example_dir = os.path.join(self.this_dir, 'ejemplos')
        self._cargar_lista_de_ejemplos()
        # LLamar cargar buscador siempre despues de cargar ejemplos
        self._cargar_buscador()

        # Senales
        self.connect(self.ui.ejecutar, QtCore.SIGNAL("clicked()"),
            self.cuando_pulsa_boton_ejecutar)
        self.connect(self.ui.fuente, QtCore.SIGNAL("clicked()"),
            self.cuando_pulsa_boton_fuente)
        self.connect(self.ui.guardar, QtCore.SIGNAL("clicked()"),
            self.cuando_pulsa_boton_guardar)
        self.connect(self.ui.arbol, QtCore.SIGNAL("itemSelectionChanged()"),
            self.cuando_cambia_seleccion)
        self.connect(self.ui.arbol,
            QtCore.SIGNAL("itemActivated(QListWidgetItem *)"),
            self.cuando_pulsa_boton_ejecutar)
        self.connect(self.ui.actionSalir, QtCore.SIGNAL("activated()"),
            self.cuando_quiere_cerrar)

        syntax.PythonHighlighter(self.ui.codigo.document())

        self._definir_estado_habilitado(True)
        self._mostrar_image_inicial()
        self._mostrar_codigo_presentacion_inicial()
        self.centrar_ventana()

    def centrar_ventana(self):
        ancho = self.size().width()
        alto = self.size().height()
        escritorio = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(
                    (escritorio.width() - ancho) / 2,
                    (escritorio.height() - alto) / 2, ancho, alto)

    def _definir_estado_habilitado(self, esta_habilitado):
        "Oculta la barra de progreso y habilita todos los controles."

        widgets = [self.locate_widget, self.ui.progreso, self.ui.ejecutar,
            self.ui.guardar, self.ui.arbol, self.ui.fuente, self.ui.codigo,
            self.ui.imagen]

        self.ui.progreso.setVisible(not esta_habilitado)

        for x in widgets:
            x.setEnabled(esta_habilitado)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return and \
        self.ui.arbol.hasFocus() and \
        self.ui.arbol.currentItem().childCount() == 0:
            self.cuando_pulsa_boton_ejecutar()

        return QtGui.QMainWindow.keyPressEvent(self, event)

    def _cargar_buscador(self):
        self.locate_widget = buscador.ExampleLocatorWidget(
            self.ejemplos, self.ui.arbol)
        self.ui.vlayout_left.addWidget(self.locate_widget)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(
            QtCore.Qt.CTRL + QtCore.Qt.Key_F), self)
        self.connect(self.locate_widget, QtCore.SIGNAL("itemFound(QString)"),
            self.buscador_resultado_encontrado)
        self.connect(shortcut, QtCore.SIGNAL("activated()"),
            self.locate_widget.setFocus)

    def _cargar_lista_de_ejemplos(self):
        self.ejemplos = {}
        self.ui.arbol.setColumnCount(1)
        self.ui.arbol.setHeaderLabels(["Nombre"])

        directorios = glob.glob(self.example_dir + '/*')

        for directorio in directorios:
            raiz = QtGui.QTreeWidgetItem([os.path.basename(directorio), ""])
            self.ui.arbol.addTopLevelItem(raiz)

            archivos = glob.glob(directorio + '/*.py')
            archivos.sort()

            for archivo in archivos:
                nombre_legible = os.path.basename(archivo).replace(".py", "")
                item = QtGui.QTreeWidgetItem([nombre_legible, archivo])
                raiz.addChild(item)
                self.ejemplos[nombre_legible] = archivo

    def _iniciar_interfaz(self):
        QtGui.QMainWindow.__init__(self)
        ui.Ui_MainWindow.__init__(self)
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

    def cuando_pulsa_boton_ejecutar(self):
        nombre_ejemplo = self._obtener_item_actual()
        self._ejecutar_ejemplo(nombre_ejemplo)

    def cuando_quiere_cerrar(self):
        sys.exit(0)

    def cuando_pulsa_boton_fuente(self):
        font = self.ui.codigo.font()
        font, ok = QtGui.QFontDialog.getFont(font)

        if ok:
            self.ui.codigo.setFont(font)

    def cuando_pulsa_boton_guardar(self):
        nombre = self._obtener_item_actual()
        path = unicode(QtGui.QFileDialog.getSaveFileName(self,
                    'Guardar ejemplo',
                    nombre,
                    "py (*.py)"))
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

    def buscador_resultado_encontrado(self, ruta):
        if ruta:
            item = self._obtener_item_desde_ruta(ruta)

            if item:
                self.ui.arbol.setCurrentItem(item)

    def _obtener_item_desde_ruta(self, ruta):
        nombres = ruta.split('/')
        categoria = nombres[-2]
        nombre = nombres[-1].replace('.py', '')

        items = self.ui.arbol.findItems(nombre, QtCore.Qt.MatchRecursive)

        if items:
            return items[0]

    def _mostrar_imagen_del_ejemplo(self, ruta):
        escena = QtGui.QGraphicsScene()
        self.ui.imagen.setScene(escena)
        pixmap = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(ruta.replace('.py', '.png')))
        #ancho = self.ui.imagen.width()
        escena.addItem(pixmap)

    def _mostrar_image_inicial(self):
        path = os.path.join(os.path.dirname(__file__), "data/_presentacion")
        self._mostrar_imagen_del_ejemplo(path)

    def _mostrar_codigo_del_ejemplo(self, nombre):
        contenido = self._obtener_codigo_del_ejemplo(nombre)
        self.ui.codigo.document().setPlainText(contenido)

    def _mostrar_codigo_presentacion_inicial(self):
        self.ui.codigo.document().setPlainText(MENSAJE_PRESENTACION)

    def _obtener_codigo_del_ejemplo(self, nombre):
        archivo = open(nombre)
        contenido = archivo.read()
        archivo.close()
        return contenido

    def _obtener_item_actual(self):
        return self.ui.arbol.currentItem().text(1)

    def _ejecutar_ejemplo(self, ruta):
        self.process = QtCore.QProcess(self)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.finished.connect(
            self._cuando_termina_la_ejecucion_del_ejemplo)
        self.process.start(sys.executable, [ruta])

        # Deshabilita todos los controles para que se pueda
        # ejecutar un ejemplo a la vez.
        self._definir_estado_habilitado(False)

    def _cuando_termina_la_ejecucion_del_ejemplo(self, estado, process):
        "Vuelve a permitir que se usen todos los botone de la interfaz."
        print self.process.readAll()
        self._definir_estado_habilitado(True)
        self.ui.arbol.setFocus()


def main():
    app = QtGui.QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
