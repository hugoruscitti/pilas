# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit

from asistente_base import Ui_Main
import pilas
import utils

class Ventana(Ui_Main):

    def setupUi(self, Main):
        Ui_Main.setupUi(self, Main)

        self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webView.connect(self.webView, QtCore.SIGNAL("linkClicked(const QUrl&)"), self.cuando_pulsa_link)
        self._cargar_pagina_principal()
        self.main = Main


    def _cargar_pagina_principal(self):
        file_path = utils.obtener_ruta_al_recurso('asistente/index.html')

        contenido = self._obtener_html(file_path)
        base_dir =  QtCore.QUrl.fromLocalFile(file_path)

        self.webView.setHtml(contenido, base_dir)

    def _obtener_html(self, file_path):
        archivo = open(file_path, "rt")
        contenido = archivo.read()
        archivo.close()
        return contenido.replace("{{VERSION}}", pilas.version())

    def cuando_pulsa_link(self, url):
        seccion = str(url.path()).split('/')[-1]

        if seccion == "interprete":
            pilas.abrir_interprete()
        elif seccion == "ejemplos":
            from ejemplos import cargador
            ventana = cargador.VentanaPrincipal()

            dialogo = QtGui.QDialog(self.main)
            ventana.setParent(dialogo)
            dialogo.show()
            dialogo.raise_()

        elif seccion == "manual":
            print "El manual"
        elif seccion == "web":
            import webbrowser
            webbrowser.open("http://www.pilas-engine.com.ar")
        else:
            print seccion, "es una opcion desconocida"


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
