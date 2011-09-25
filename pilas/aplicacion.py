import sys
import window_base as window
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
#import pilas



class Window(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = window.Ui_Window()
        self.ui.setupUi(self)


        #self.ui.ventana = pilas.obtener_widget()
        # Agrega un nuevo widget al layout existente.
        #label = QtGui.QLabel(self.ui.centralwidget)
        #self.ui.layout.addWidget(label)
        #label.setText("Hola")

def main():
    app = QtGui.QApplication(sys.argv)
    ventana = Window()
    ventana.show()
    app.exec_()  
