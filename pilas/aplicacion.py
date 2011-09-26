import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import pilas
from pilas.console import console_widget


class Window(QtGui.QWidget):

    def __init__(self, parent=None, pilas_width=320, pilas_height=240):
        QtGui.QWidget.__init__(self, parent)

        vbox = QtGui.QVBoxLayout(self)
        pilas.iniciar(usar_motor='qt')
        ventana_pilas = pilas.mundo.motor

        ventana_pilas.setMinimumWidth(pilas_width)
        ventana_pilas.setMinimumHeight(pilas_height)

        horizontalLayout = QtGui.QHBoxLayout()
        spacer1 = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacer1)

        horizontalLayout.addWidget(ventana_pilas)

        spacer2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacer2)

        vbox.addLayout(horizontalLayout)

        #vbox.addWidget(self.horizontalLayout)
        #hbox.addWidget(ventana_pilas)

        #Crear actor
        self.mono = pilas.actores.Mono()
        pilas.eventos.click_de_mouse.conectar(self.sonreir)

        # Agrega la Consola
        locals = {'pilas': pilas, 'mono': self.mono}
        self.consoleWidget = console_widget.ConsoleWidget(locals)

        vbox.addWidget(self.consoleWidget)

        #self.ui.ventana = pilas.obtener_widget()
        # Agrega un nuevo widget al layout existente.
        #label = QtGui.QLabel(self.ui.centralwidget)
        #self.ui.layout.addWidget(label)
        #label.setText("Hola")

    def sonreir(self, evento):
        self.mono.sonreir()


def main():
    app = QtGui.QApplication(sys.argv)
    ventana = Window()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()
