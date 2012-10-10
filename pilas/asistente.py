# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import sys
import os
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

        self.webView.setAcceptDrops(False)
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
        comando = " ".join([sys.executable, sys.argv[0], '-i'])
        self._ejecutar_comando(comando)

    def ejecutar_script(self, nombre_archivo_script):
        comando = " ".join([sys.executable, sys.argv[0], '-i', str(nombre_archivo_script)])
        self._ejecutar_comando(comando)

    def _ejecutar_comando(self, comando):
        "Ejecuta un comando en segundo plano."
        self.proceso = QtCore.QProcess()
        self.proceso.startDetached(comando)

    def _cuando_selecciona_abrir_manual(self):
        base_dir = str(QtCore.QDir.homePath())
        ruta_al_manual = os.path.join(base_dir, 'pilas.pdf')

        try:
            ruta = pilas.utils.obtener_ruta_al_recurso(ruta_al_manual)
            pilas.utils.abrir_archivo_con_aplicacion_predeterminada(ruta)
        except IOError:
            titulo = "Error, no se encuentra el manual"
            mensaje = u"Lo siento, no se encuentra el manual en tu equipo. ¿Quieres descargarlo?"
            respuesta = QtGui.QMessageBox.question(self.main, titulo, mensaje,
                            QtGui.QMessageBox.Yes,
                            QtGui.QMessageBox.No)

            if respuesta == QtGui.QMessageBox.Yes:
                url = "http://media.readthedocs.org/pdf/pilas/latest/pilas.pdf"
                pilas.utils.descargar_archivo_desde_internet(self.main, url, ruta_al_manual)



class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAcceptDrops(True)

    def definir_receptor_de_comandos(self, ui):
        self.ui = ui

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        super(MainWindow, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.ui.ejecutar_script(url.path())
            event.acceptProposedAction()
        else:
            super(MainWindow,self).dropEvent(event)

def ejecutar():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("pilas-engine")

    main = MainWindow()
    ui = VentanaAsistente()
    main.definir_receptor_de_comandos(ui)
    ui.setupUi(main)

    main.show()
    main.raise_()
    app.exec_()
