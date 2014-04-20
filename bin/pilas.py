import sys
import signal
from PyQt4 import QtGui

# Permitiendo cerrar pilas usando CTRL+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

sys.path.append('./')
sys.path.append('../')

import pilasengine

app = QtGui.QApplication(sys.argv)
asistente = pilasengine.abrir_asistente()
sys.exit(app.exec_())