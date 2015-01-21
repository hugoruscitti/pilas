# -*- encoding: utf-8 -*-
import sys
sys.path.append('./')
sys.path.append('../')
from PyQt4 import QtGui
from interfaz_base import Ui_MainWindow as Base

import pilasengine

class Ventana(Base):

    def __init__(self):
        Base.__init__(self)

    def setupUi(self, MainWindow):
        Base.setupUi(self, MainWindow)

    def agregar_widget(self, widget):
        self.canvas.addWidget(widget)
        self.canvas.setCurrentWidget(widget)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()

    ui = Ventana()
    ui.setupUi(MainWindow)

    pilas = pilasengine.iniciar()

    widget_de_pilas = pilas.obtener_widget()
    ui.agregar_widget(widget_de_pilas)
    widget_de_pilas.show()

    aceituna = pilas.actores.Aceituna()
    mono = pilas.actores.Mono()

    MainWindow.show()
    MainWindow.raise_()
    sys.exit(app.exec_())
