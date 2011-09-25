import sys
import window_base as window
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
import pilas



class Window(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = window.Ui_Window()
        self.ui.graphicsView = QtGui.QTextEdit()
        self.ui.setupUi(self)
        self.ui.graphicsView.close()
        #self.ui.verticalLayout.removeWidget(self.ui.graphicsView)
        pilas.iniciar(usar_motor='qt')
        ventana_pilas = pilas.mundo.motor
        ventana_pilas.setFixedHeight(400)
        self.mono = pilas.actores.Mono()

        pilas.eventos.click_de_mouse.conectar(self.sonreir)

        self.ui.verticalLayout.insertWidget(0, ventana_pilas)



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
