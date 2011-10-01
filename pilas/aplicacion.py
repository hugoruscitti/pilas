import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import pilas
from console import console_widget

class Window(QtGui.QWidget):

    def __init__(self, parent=None, pilas_width=640, pilas_height=480):
        QtGui.QWidget.__init__(self, parent)

        vbox = QtGui.QVBoxLayout(self)
        pilas.iniciar(usar_motor='qtsugar')
        ventana_pilas = pilas.mundo.motor

        ventana_pilas.setMinimumWidth(pilas_width)
        ventana_pilas.setMinimumHeight(pilas_height)

        expandir = QtGui.QSizePolicy.Expanding
        minimo = QtGui.QSizePolicy.Minimum

        horizontalLayout = QtGui.QHBoxLayout()
        spacer1 = QtGui.QSpacerItem(58, 20, expandir, minimo)
        horizontalLayout.addItem(spacer1)

        horizontalLayout.addWidget(ventana_pilas.widget)

        spacer2 = QtGui.QSpacerItem(40, 20, expandir, minimo)
        horizontalLayout.addItem(spacer2)

        vbox.addLayout(horizontalLayout)

        self.mono = pilas.actores.Mono()

        locals = {'pilas': pilas, 'mono': self.mono}

        self.consoleWidget = console_widget.ConsoleWidget(locals, ventana_pilas)
        vbox.addWidget(self.consoleWidget)

        self.ventana_pilas = ventana_pilas
        self.setWindowTitle("Pilas engine")

def main():
    app = QtGui.QApplication(sys.argv)
    ventana = Window()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()
