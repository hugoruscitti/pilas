# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit

from asistente_base import Ui_Main
import pilas
import utils

class VentanaAsistente(Ui_Main):

    def setupUi(self, main):
        Ui_Main.setupUi(self, main)

        self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webView.connect(self.webView, QtCore.SIGNAL("linkClicked(const QUrl&)"), self.cuando_pulsa_link)
        self._cargar_pagina_principal()
        self.main = main

    def _cargar_pagina_principal(self):
        file_path = utils.obtener_ruta_al_recurso('asistente/index.html')

        contenido = self._obtener_html(file_path)
        base_dir =  QtCore.QUrl.fromLocalFile(file_path)

        self.webView.setHtml(contenido, base_dir)

    def _obtener_html(self, file_path):
        archivo = open(file_path, "rt")
        contenido = archivo.read()
        archivo.close()
        return contenido.replace("{{VERSION}}", pilas.version()).decode('utf8')

    def cuando_pulsa_link(self, url):
        seccion = str(url.path()).split('/')[-1]

        if seccion == "interprete":
            pilas.abrir_interprete()
        elif seccion == "ejemplos":
            self._cuando_selecciona_ejemplos()
        elif seccion == "manual":
            self._cuando_selecciona_abrir_manual()
        elif seccion == "web":
            import webbrowser
            webbrowser.open("http://www.pilas-engine.com.ar")
        else:
            print seccion, "es una opcion desconocida"

    def _cuando_selecciona_ejemplos(self):
        from ejemplos import cargador
        cargador.main(self.main)

    def _cuando_selecciona_abrir_manual(self):
        try:
            ruta = pilas.utils.obtener_ruta_al_recurso('pilas.pdf')
            pilas.utils.abrir_archivo_con_aplicacion_predeterminada(ruta)
        except IOError as e:
            dialogo = QtGui.QMessageBox.warning(self.main, "Error, no se encuentra el manual", "Lo siento, no se encuentra el archivo 'pilas.pdf' intente visitando la web del proyecto.")

app = None

def ejecutar():
    global app

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = VentanaAsistente()
    ui.setupUi(Dialog)

    Dialog.show()
    Dialog.raise_()
    app.exec_()
