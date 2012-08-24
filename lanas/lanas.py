# -*- coding: utf-8 -*-
import sys
sys.path.append("kanzen")

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import interprete

def main():
    app = QApplication(sys.argv)
    win = interprete.Ventana(None, "Lanas")
    win.show()
    win.raise_()
    sys.exit(app.exec_())
