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
from api_base import Ui_ManualWindow
from PyQt4 import QtWebKit
from PyQt4 import QtNetwork

import pilasengine

class VentanaApi(Ui_ManualWindow):

    def setupUi(self, main):
        self.main = main
        Ui_ManualWindow.setupUi(self, main)
        self._habilitar_inspector_web()
        self.cargar_api()

    def cargar_api(self):
        file_path = pilasengine.utils.obtener_ruta_al_recurso('api/index.html')
        file_path = os.path.abspath(file_path)

        base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        self.webView.load(base_dir)
        self.webView.history().setMaximumItemCount(0)

    def _habilitar_inspector_web(self):
        print "habilitando inspector"
        QtWebKit.QWebSettings.globalSettings()
        settings = QtWebKit.QWebSettings.globalSettings()
        settings.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        try:
            settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)
        except AttributeError:
            pass  # Arreglo para funcionar en ubuntu 10.04

def abrir():
    MainWindow = QtGui.QMainWindow()

    ui = VentanaApi()
    ui.setupUi(MainWindow)

    MainWindow.show()
    MainWindow.raise_()
    pilasengine.utils.destacar_ventanas()

    return MainWindow
