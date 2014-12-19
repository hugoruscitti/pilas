# -*- encoding: utf-8 -*-
#
# Inicia lanas para realizar una prueba
# rápida.

import sys
from PyQt4 import QtGui

import lanas


app = QtGui.QApplication(sys.argv)

widget = lanas.WidgetLanas(scope={"lanas": lanas})
widget.show()
widget.raise_()

sys.exit(app.exec_())
