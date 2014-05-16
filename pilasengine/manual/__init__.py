# -*- coding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
import sys

from PyQt4 import QtCore, QtGui
from manual_base import Ui_ManualWindow

import pilasengine

class VentanaManual(Ui_ManualWindow):

    def setupUi(self, main):
        self.main = main
        Ui_ManualWindow.setupUi(self, main)
        self.cargar_manual()

    def cargar_manual(self):
        file_path = pilasengine.utils.obtener_ruta_al_recurso('manual/index.html')
        file_path = os.path.abspath(file_path)

        base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        self.webView.load(base_dir)
        self.webView.history().setMaximumItemCount(0)


def abrir():
    MainWindow = QtGui.QMainWindow()

    ui = VentanaManual()
    ui.setupUi(MainWindow)

    MainWindow.show()
    MainWindow.raise_()

    return MainWindow