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
import threading
import syntax


class VentanaPrincipal(QtGui.QMainWindow, ui.Ui_MainWindow):

    def __init__(self):
        self._iniciar_interfaz()
        self._cargar_lista_de_ejemplos()

        # Senales
        self.connect(self.ui.ejecutar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_boton_ejecutar)
        self.connect(self.ui.guardar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_boton_guardar)
        self.connect(self.ui.lista, QtCore.SIGNAL("itemSelectionChanged()"), self.cuando_cambia_seleccion)
        self.connect(self.ui.lista, QtCore.SIGNAL("itemActivated(QListWidgetItem *)"), self.cuando_pulsa_boton_ejecutar)

        syntax.PythonHighlighter(self.ui.codigo.document())

        self._definir_estado_habilitado(True)

    def _definir_estado_habilitado(self, esta_habilitado):
        "Oculta la barra de progreso y habilita todos los controles."

        widgets = [self.ui.progreso, self.ui.ejecutar, self.ui.guardar, 
            self.ui.lista, self.ui.codigo, self.ui.imagen]

        self.ui.progreso.setVisible(not esta_habilitado)

        for x in widgets:
            x.setEnabled(esta_habilitado)

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
        self._ejecutar_ejemplo(nombre_ejemplo)


    def cuando_pulsa_boton_guardar(self):
        nombre = self._obtener_item_actual()
        path = unicode(QtGui.QFileDialog.getSaveFileName(self, 
                    'Guardar ejemplo',
                    nombre + ".py",
                    "py (*.py)"))
        contenido = self._obtener_codigo_del_ejemplo(nombre)

        archivo = open(path, "wt")
        archivo.write(contenido)
        archivo.close()

    def cuando_cambia_seleccion(self):
        nombre = self._obtener_item_actual()
        self._mostrar_codigo_del_ejemplo(nombre)
        self._mostrar_imagen_del_ejemplo(nombre)

    def _mostrar_imagen_del_ejemplo(self, nombre):
        escena = QtGui.QGraphicsScene()
        self.ui.imagen.setScene(escena)
        pixmap = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('ejemplos/capturas/' + nombre + '.png'))
        escena.addItem(pixmap);

    def _mostrar_codigo_del_ejemplo(self, nombre):
        contenido = self._obtener_codigo_del_ejemplo(nombre)
        self.ui.codigo.document().setPlainText(contenido)

    def _obtener_codigo_del_ejemplo(self, nombre):
        archivo = open('ejemplos/' + nombre + '.py', 'rt')
        contenido = archivo.read()
        archivo.close()
        return contenido

    def _obtener_item_actual(self):
        return self.ui.lista.currentItem().text()

    def _ejecutar_ejemplo(self, ejemplo):
        process = QtCore.QProcess(self)
        process.finished.connect(self._cuando_termina_la_ejecucion_del_ejemplo)
        process.start(sys.executable, ['ejemplos/' + ejemplo])

        # Deshabilita todos los controles para que se pueda
        # ejecutar un ejemplo a la vez.
        self._definir_estado_habilitado(False)

    def _cuando_termina_la_ejecucion_del_ejemplo(self, estado):
        "Vuelve a permitir que se usen todos los botone de la interfaz."
        self._definir_estado_habilitado(True)
        self.ui.lista.setFocus()
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec_())

