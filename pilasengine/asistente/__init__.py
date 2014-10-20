# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import sys
import os
import webbrowser

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from PyQt4 import QtNetwork

from asistente_base import Ui_AsistenteWindow as Base
import pilasengine

class Interlocutor(QtCore.QObject):
    """Representa el objeto auxiliar que permite la comunicación js/Qt

    Esta clase se utiliza para cominicar a javascript (dentro del
    webview) con los objetos python dentro de pilas.
    """

    def iniciar_con_ventana(self, ventana):
        self.manual = None
        self.interprete = None
        self.ventana = ventana
        self.configuracion = None

    @QtCore.pyqtSlot()
    def abrir_interprete(self):
        #if not self.interprete:
        #    self.interprete = pilasengine.abrir_interprete()
        #else:
        #    self.interprete.show()
        #    self.interprete.raise_()
        self.interprete = pilasengine.abrir_interprete()

    @QtCore.pyqtSlot(str)
    def abrir_ejemplo(self, juego):
        juego = str(juego)
        ruta_al_ejemplo = os.path.join(os.path.dirname(__file__), '..', 'ejemplos/' + juego + '.py')
        self.ventana.abrir_ejemplo(ruta_al_ejemplo)

    @QtCore.pyqtSlot()
    def abrir_manual(self):
        if not self.manual:
            self.manual = pilasengine.abrir_manual()
        else:
            self.manual.show()
            self.manual.raise_()

    @QtCore.pyqtSlot()
    def abrir_configuracion(self):
        self.configuracion = pilasengine.abrir_configuracion(self.ventana.MainWindow)

    @QtCore.pyqtSlot()
    def abrir_sitio_de_pilas(self):
        webbrowser.open("http://www.pilas-engine.com.ar")

    @QtCore.pyqtSlot(str, result=str)
    def obtener_codigo_del_ejemplo(self, juego):
        juego = str(juego)
        ruta_al_ejemplo = os.path.join(os.path.dirname(__file__), '..', 'ejemplos/' + juego + '.py')
        archivo = open(ruta_al_ejemplo, "rt")
        contenido = archivo.read()
        archivo.close()
        return contenido

    @QtCore.pyqtSlot(result=str)
    def obtener_ejemplos(self):
        directorio_de_ejemplos = os.path.join(os.path.dirname(__file__), '../ejemplos')
        juegos = os.listdir(directorio_de_ejemplos)
        juegos = [j.replace('.py', '') for j in juegos if j.endswith('.py') and not j.startswith('__')]
        juegos = '{"ejemplos": ' + str(juegos).replace("'", '"') + "}"
        return str(juegos)

class VentanaAsistente(Base):
    """Representa la ventana principal del asistente."""

    def __init__(self):
        Base.__init__(self)

    def setupUi(self, MainWindow):
        Base.setupUi(self, MainWindow)
        self.MainWindow = MainWindow

        self.interlocutor = Interlocutor()
        self.interlocutor.iniciar_con_ventana(self)

        objeto_js = self.webView.page().mainFrame().javaScriptWindowObjectCleared
        objeto_js.connect(self._vincular_con_javascript)

        self._cargar_pagina_principal()
        self._habilitar_inspector_web()

        self.webView.setAcceptDrops(False)
        self._deshabilitar_barras_de_scroll()

        self.webView.history().setMaximumItemCount(0)
        self.webView.setAcceptDrops(True)

        self.webView.dragEnterEvent = self.dragEnterEvent
        self.webView.dragLeaveEvent = self.dragLeaveEvent
        self.webView.dropEvent = self.dropEvent

    def _vincular_con_javascript(self):
        self.webView.page().mainFrame().addToJavaScriptWindowObject("interlocutor", self.interlocutor)

    def _consultar_ultima_version_del_servidor(self):
        direccion = QtCore.QUrl("https://raw.github.com/hugoruscitti/pilas/gh-pages/version.json")
        self.manager = QtNetwork.QNetworkAccessManager(self.main)
        self.manager.get(QtNetwork.QNetworkRequest(direccion))

        self.manager.connect(self.manager, QtCore.SIGNAL("finished(QNetworkReply*)"),
                self._cuando_termina_de_consultar_version)

    def _habilitar_inspector_web(self):
        QtWebKit.QWebSettings.globalSettings()
        settings = QtWebKit.QWebSettings.globalSettings()
        settings.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        try:
            settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)
        except AttributeError:
            pass  # Arreglo para funcionar en ubuntu 10.04

    def _deshabilitar_barras_de_scroll(self):
        self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAsNeeded)

    def _cargar_pagina_principal(self):
        file_path = pilasengine.utils.obtener_ruta_al_recurso('asistente/index.html')
        self.webView.load(QtCore.QUrl.fromLocalFile(file_path))

    def observar_cambios_de_archivos(self, nombre_archivo_script, directorio_trabajo):
        for f in self.watcher.files():
            self.watcher.removePath(f)

        self.watcher.addPath(nombre_archivo_script)
        #(nombre_archivo_script, directorio_trabajo))

    def evaluar_javascript(self, codigo):
        self.webView.page().mainFrame().evaluateJavaScript(codigo)

    def definir_receptor_de_comandos(self, ui):
        self.ui = ui

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.evaluar_javascript("resaltar_caja_destino_para_soltar(true);")

    def dragLeaveEvent(self, event):
        self.evaluar_javascript("resaltar_caja_destino_para_soltar(false);")

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                archivo = url.toLocalFile()

                if not unicode(archivo).endswith('.py'):
                    QtGui.QMessageBox.critical(self.MainWindow, "Error", "Solo se aceptan archivos terminados con .py")
                else:
                    self._ejecutar_programa_con_livereload(unicode(archivo))
                    event.acceptProposedAction()

        self.evaluar_javascript("resaltar_caja_destino_para_soltar(false);")

    def _ejecutar_programa_con_livereload(self, archivo):
        self.programa = pilasengine.abrir_script_con_livereload(archivo)

    def abrir_ejemplo(self, archivo):
        self.programa = pilasengine.abrir_script_con_livereload(archivo)

def abrir():
    MainWindow = QtGui.QMainWindow()

    ui = VentanaAsistente()
    ui.setupUi(MainWindow)

    MainWindow.show()
    MainWindow.raise_()

    return MainWindow
