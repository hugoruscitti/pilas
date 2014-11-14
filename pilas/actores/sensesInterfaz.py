import pilas
import sys
from PyQt4 import QtGui, QtCore, uic

class Sense(QtGui.QMainWindow):
    def __init__(self, unRobot):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("/usr/local/lib/python2.7/dist-packages/pilas-0.81-py2.7.egg/pilas/data/senses.ui")
        self.ui.show()
        self._mostrarInfo()
        aelf.robot = unRobot

    def _mostrarInfo(self):
        
        def mostrarBateria():
            self.ui.bateria.display( "{0:.2f}".f , self.robot.battery())

        def mostrarPing():
            self.ui.nping.display( "{0:.2f}".f , self.robot.ping())

        def mostrarSensoresDeLinea():
            izq, der = self.robot.getLine()
            self.ui.iline.display( "{0:.2f}".f , izq)
            self.ui.dline.display( "{0:.2f}".f , der)

        while True:
             pilas.escena_actual().tareas.condicional(3, mostrarBateria)
	     pilas.escena_actual().tareas.condicional(1, mostrarPing)
	     pilas.escena_actual().tareas.condicional(1, mostrarSensoresDeLinea)


# if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
#    from robot import *
#    from board  import *
#    from pilas.actores import Pizarra
#    import pilas
#    from pilas.actores import Actor

#    b = Board("/dev/ttyUSB0")
#    r = Robot(b, 1)

#    wentana = sense(r)
    
#    sys.exit(app.exec_())




