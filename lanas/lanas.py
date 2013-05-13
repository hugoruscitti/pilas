# -*- coding: utf-8 -*-
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import interprete

def main(with_log=False):
    app = QApplication(sys.argv)
    app.setApplicationName('Lanas')
    win = interprete.Ventana(with_log=with_log)
    win.show()
    win.raise_()
    sys.exit(app.exec_())
