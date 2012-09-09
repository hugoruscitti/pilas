# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit

from asistente_base import Ui_AsistenteWindow
import pilas
import utils
import interprete
from ejemplos import cargador

class VentanaAsistente(Ui_AsistenteWindow):

    def setupUi(self, main):
        self.main = main
        Ui_AsistenteWindow.setupUi(self, main)

        self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webView.connect(self.webView, QtCore.SIGNAL("linkClicked(const QUrl&)"), self.cuando_pulsa_link)
        self._cargar_pagina_principal()
        self._deshabilitar_barras_de_scroll()
        pilas.utils.centrar_ventana(main)
        self.statusbar.showMessage(u"Versión " + pilas.version())

    def _deshabilitar_barras_de_scroll(self):
        self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)

    def _cargar_pagina_principal(self):
        file_path = utils.obtener_ruta_al_recurso('asistente/index.html')

        contenido = self._obtener_html(file_path)
        base_dir =  QtCore.QUrl.fromLocalFile(file_path)

        self.webView.setHtml(contenido, base_dir)

    def _obtener_html(self, file_path):
        archivo = open(file_path, "rt")
        contenido = archivo.read()
        archivo.close()
        return contenido.decode('utf8')

    def cuando_pulsa_link(self, url):
        seccion = str(url.path()).split('/')[-1]

        if seccion == "interprete":
            self._cuando_selecciona_interprete()
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
        cargador.main(self.main)

    def _cuando_selecciona_interprete(self):
        interprete.main(self.main)

    def _cuando_selecciona_abrir_manual(self):
        try:
            ruta = pilas.utils.obtener_ruta_al_recurso('pilas.pdf')
            pilas.utils.abrir_archivo_con_aplicacion_predeterminada(ruta)
        except IOError:
            titulo = "Error, no se encuentra el manual"
            mensaje = "Lo siento, no se encuentra el archivo 'pilas.pdf' intente visitando la web del proyecto."
            QtGui.QMessageBox.warning(self.main, titulo, mensaje)


def ejecutar():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("pilas-engine")

    main = QtGui.QMainWindow()
    ui = VentanaAsistente()
    ui.setupUi(main)

    main.show()
    main.raise_()
    app.exec_()
