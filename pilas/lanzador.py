# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from .lanzador_base import Ui_Dialog
from . import utils

class Ventana(Ui_Dialog):

    def setupUi(self, Dialog):
        Ui_Dialog.setupUi(self, Dialog)
        self.ha_aceptado = False
        self._quitar_barras_scroll()
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.acepta)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def acepta(self):
        self.ha_aceptado = True

    def obtener_seleccion(self):
        motor = ['qtgl', 'qt']
        modo = [False, True]
        audio = ['gst', 'phonon', 'deshabilitado']

        i = self.comboBox.currentIndex()
        j = self.comboBox_2.currentIndex()
        k = self.comboBox_3.currentIndex()

        return (motor[i], modo[j], audio[k])

    def _quitar_barras_scroll(self):
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def mostrar_imagen(self, ruta):
        escena = QtGui.QGraphicsScene()
        self.graphicsView.setScene(escena)
        pixmap = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(ruta))

        # Define el size para la imagen
        width = pixmap.boundingRect().width()
        height = pixmap.boundingRect().height()
        self.graphicsView.setFixedSize(width, height)

        escena.addItem(pixmap)


app = None


def ejecutar(imagen, titulo):
    global app

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    Dialog.setWindowTitle(titulo)
    ui = Ventana()
    ui.setupUi(Dialog)

    if imagen:
        ruta_a_imagen = utils.obtener_ruta_al_recurso(imagen)
        ui.mostrar_imagen(ruta_a_imagen)

    Dialog.show()
    Dialog.raise_()
    app.exec_()

    if not ui.ha_aceptado:
        sys.exit(0)

    return ui.obtener_seleccion()
