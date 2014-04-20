import sys
from PyQt4 import QtGui

sys.path.append('./')
sys.path.append('../')

import pilasengine

app = QtGui.QApplication(sys.argv)
asistente = pilasengine.abrir_asistente()
sys.exit(app.exec_())