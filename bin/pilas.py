import sys
import signal
from PyQt4 import QtGui

# Permitiendo cerrar pilas usando CTRL+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

sys.path.append('./')
sys.path.append('../')

import pilasengine

app = QtGui.QApplication(sys.argv)

if '-i' in sys.argv:
    from pilasengine import interprete
    _ = interprete.abrir()
else:
    _ = pilasengine.abrir_asistente()

sys.exit(app.exec_())