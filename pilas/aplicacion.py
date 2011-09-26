import sys

from PyQt4 import QtGui

import pilas
from pilas.console import console_widget


class Window(QtGui.QWidget):

    def __init__(self, parent=None, pilas_height=500):
        QtGui.QWidget.__init__(self, parent)
        vbox = QtGui.QVBoxLayout(self)
        pilas.iniciar(usar_motor='qt')
        ventana_pilas = pilas.mundo.motor
        ventana_pilas.setMinimumHeight(pilas_height)
        vbox.addWidget(ventana_pilas)

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
