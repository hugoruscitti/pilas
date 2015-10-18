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
import json

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
        self.api = None

    @QtCore.pyqtSlot()
    def abrir_interprete(self):
        self.interprete = pilasengine.abrir_interprete()

    @QtCore.pyqtSlot()
    def abrir_editor(self):
        self.interprete = pilasengine.abrir_editor()

    @QtCore.pyqtSlot(str)
    def abrir_ejemplo(self, juego):
        juego = str(juego)
        ruta_al_ejemplo = os.path.join(os.path.dirname(__file__), '..', 'ejemplos/' + juego + '.py')
        ruta_al_ejemplo = os.path.abspath(ruta_al_ejemplo)
        self.ventana.abrir_ejemplo(ruta_al_ejemplo)

    @QtCore.pyqtSlot()
    def abrir_manual(self):
        if not self.manual:
            self.manual = pilasengine.abrir_manual()
        else:
            self.manual.show()
            self.manual.raise_()

    @QtCore.pyqtSlot()
    def abrir_api(self):
        if not self.api:
            self.api = pilasengine.abrir_api()
        else:
            self.api.show()
            self.api.raise_()

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

    @QtCore.pyqtSlot(result=str)
    def obtener_version_desde_el_servidor(self):
        return self.version_del_servidor

    def definir_version(self, version, version_local):
        codigo = "definir_version('VR', 'VL')".replace('VR', version).replace('VL', version_local)
        self.ventana.webView.page().mainFrame().evaluateJavaScript(codigo)


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

        self.webView.loadFinished.connect(self._iniciar_consulta_de_version)
        self.centrar_ventana(MainWindow)

    def centrar_ventana(self, widget):
        """Coloca la ventana o widget directamente en el centro del escritorio.

        :param widget: Widget que representa la ventana.
        """
        from PyQt4 import QtGui
        desktop = QtGui.QApplication.desktop()
        centro = desktop.screen().rect().center()

        if centro.x() > 1000:
            centro.setX(centro.x() / 2)

        widget.move(centro - widget.rect().center())

    def _iniciar_consulta_de_version(self):
        self._consultar_ultima_version_del_servidor()

    def _vincular_con_javascript(self):
        self.webView.page().mainFrame().addToJavaScriptWindowObject("interlocutor", self.interlocutor)

    def _consultar_ultima_version_del_servidor(self):
        direccion = QtCore.QUrl("https://raw.githubusercontent.com/hugoruscitti/pilas/gh-pages/version.json")
        self.manager = QtNetwork.QNetworkAccessManager(self.MainWindow)
        self.manager.get(QtNetwork.QNetworkRequest(direccion))

        self.manager.connect(self.manager, QtCore.SIGNAL("finished(QNetworkReply*)"),
                self._cuando_termina_de_consultar_version)

    def _cuando_termina_de_consultar_version(self, respuesta):
        respuesta_como_texto = respuesta.readAll().data()

        try:
            respuesta_como_json = json.loads(str(respuesta_como_texto))
            version_en_el_servidor = respuesta_como_json['nueva_version']
            self.interlocutor.definir_version(version_en_el_servidor, pilasengine.VERSION)
        except ValueError, e:
            self.interlocutor.definir_version("", pilasengine.VERSION)

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
                    print(u"ERROR, se envió el archivo " + unicode(archivo))
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
    pilasengine.utils.destacar_ventanas()
    return MainWindow
