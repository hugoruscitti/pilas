# -*- encoding: utf-8 -*-
import sys

from PyQt4 import QtGui

import pilasengine


class VentanaAsistente(QtGui.QWidget):

    def __init__(self):
        super(VentanaAsistente, self).__init__()
        self.initUI()

    def agregar_widget(self, widget):
        self.widget = widget
        self.hbox.addWidget(self.widget, 0)

    def initUI(self):
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle('Burning widget')
        self.show()
        self.raise_()


def main():
    app = QtGui.QApplication(sys.argv)
    ventana = VentanaAsistente()

    # similar a la funcion "iniciar" pero simplemente
    # arma el widget para utilizar dentro de una aplicacion.
    pilas = pilasengine.iniciar()

    widget_de_pilas = pilas.obtener_widget()
    ventana.agregar_widget(widget_de_pilas)
    widget_de_pilas.show()

    pilas.actores.Aceituna()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
