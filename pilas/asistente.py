# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui

from asistente_base import Ui_Main

class Ventana(Ui_Main):

    def setupUi(self, Main):
        Ui_Main.setupUi(self, Main)



app = None

def ejecutar():
    global app

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ventana()
    ui.setupUi(Dialog)

    Dialog.show()
    Dialog.raise_()
    app.exec_()
