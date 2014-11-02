# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import sys
import os
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
import json

from .asistente_base import Ui_AsistenteWindow
import pilas
from . import utils

class VentanaAsistente(Ui_AsistenteWindow):

    def setupUi(self, main):
        self.nombre_archivo_script = ""
        self.main = main
        Ui_AsistenteWindow.setupUi(self, main)
        main.setWindowTitle("pilas-engine")
        main.resize(550, 442)

        self.webView.setAcceptDrops(False)
        self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateExternalLinks)
        self.webView.connect(self.webView, QtCore.SIGNAL("linkClicked(const QUrl&)"), self.cuando_pulsa_link)
        self._cargar_pagina_principal()
        self._deshabilitar_barras_de_scroll()
        pilas.utils.centrar_ventana(main)
        self.statusbar.showMessage(u"Versión " + pilas.version())
        self._habilitar_inspector_web()
        self.salir_action.connect(self.salir_action, QtCore.SIGNAL("triggered()"), self.salir)
        self._consultar_ultima_version_del_servidor()
        self.process = None
        self.watcher = QtCore.QFileSystemWatcher(parent=self.main)
        self.watcher.connect(self.watcher, QtCore.SIGNAL('fileChanged(const QString&)'), self._reiniciar_proceso)
        self.webView.history().setMaximumItemCount(0)

    def _consultar_ultima_version_del_servidor(self):
        direccion = QtCore.QUrl("https://raw.github.com/hugoruscitti/pilas/gh-pages/version.json")
        self.manager = QtNetwork.QNetworkAccessManager(self.main)
        self.manager.get(QtNetwork.QNetworkRequest(direccion))

        self.manager.connect(self.manager, QtCore.SIGNAL("finished(QNetworkReply*)"),
                self._cuando_termina_de_consultar_version)

    def _cuando_termina_de_consultar_version(self, respuesta):
        respuesta_como_texto = respuesta.readAll().data()
        try:
            respuesta_como_json = json.loads(str(respuesta_como_texto))

            version_en_el_servidor = float(respuesta_como_json['version'])
            version_instalada = float(pilas.pilasversion.VERSION)

            if version_en_el_servidor == version_instalada:
                mensaje = "- actualizada"
            elif version_en_el_servidor < version_instalada:
                mensaje = u"- desarrollo (versión estable en la web: %.2f)" %(version_en_el_servidor)
            else:
                mensaje = u"- desactualizada: la version %.2f ya está disponible en la web!)" %(version_en_el_servidor)
        except ValueError:
            mensaje = u"(sin conexión a internet)"

        self.statusbar.showMessage(u"Versión " + pilas.version() + " " + mensaje)


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
        file_path = utils.obtener_ruta_al_recurso('asistente/index.html')
        self.webView.load(QtCore.QUrl.fromLocalFile(file_path))
        # TODO: convierto la ruta en absoluta para que mac desde py2app
        #       pueda interpretar correctamente las imagenes.
        #file_path = os.path.abspath(file_path)

        #contenido = self._obtener_html(file_path)
        #base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        #self.webView.setHtml(contenido, base_dir)

    def _obtener_html(self, file_path):
        archivo = open(file_path, "rt")
        contenido = archivo.read()
        archivo.close()
        return contenido.decode('utf8')

    def cuando_pulsa_link(self, url):
        seccion = str(url.path()).split('/')[-1]

        if seccion == "interprete":
            self._cuando_selecciona_interprete()
        elif seccion == "manual":
            self._cuando_selecciona_abrir_manual()
        elif seccion == "tutoriales":
            self._cuando_selecciona_abrir_tutoriales()
        elif seccion == "web":
            import webbrowser
            webbrowser.open("http://www.pilas-engine.com.ar")
        else:
            partes = url.path().split('/')

            if len(partes) == 4:
                accion = partes[1]
                categoria = partes[2]
                ejemplo = partes[3]

                if accion == "ejecutar":
                    self._ejecutar_ejemplo(str(categoria), str(ejemplo))
                elif accion == "codigo":
                    self._mostrar_codigo(str(categoria), str(ejemplo))
                else:
                    print(accion, "sobre el ejemplo", ejemplo)
            else:
                raise Exception(seccion + "es una opcion desconocida")

    def _ejecutar_ejemplo(self, categoria, nombre):
        """Intenta ejecutar un programa de ejemplo en base a la categoria y nombre.

        Internamente, esta funcion intenta buscar un archivo dentro de la
        ruta "../ejemplos/ejemplos/{categoria}/{nombre}.py".
        """
        if sys.platform == "darwin":
            ruta = self._obtener_ruta_al_ejemplo(categoria, nombre)
            pilas.interprete.cargar_ejemplo(self.main, True, ruta)
        else:
            try:
                ruta = self._obtener_ruta_al_ejemplo(categoria, nombre)

                self.process = QtCore.QProcess(self.main)
                self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
                self.process.finished.connect(self._cuando_termina_la_ejecucion_del_ejemplo)
                self.process.start(sys.executable, [ruta], QtCore.QIODevice.ReadWrite)
            except Exception as name:
                QtGui.QMessageBox.critical(self.main, "Error", str(name))

    def _mostrar_codigo(self, categoria, nombre):
        try:
            ruta = self._obtener_ruta_al_ejemplo(categoria, nombre)
            file_path = utils.obtener_ruta_al_recurso('asistente/codigo.html')
            # TODO: convierto la ruta en absoluta para que mac desde py2app
            #       pueda interpretar correctamente las imagenes.
            file_path = os.path.abspath(file_path)

            contenido = self._obtener_html(file_path)

            import codecs
            archivo_codigo = codecs.open(ruta, "r", "utf-8")
            contenido_codigo = archivo_codigo.read()
            archivo_codigo.close()
            contenido = contenido.replace("{codigo}", contenido_codigo)
            base_dir =  QtCore.QUrl.fromLocalFile(file_path)
            self.webView.setHtml(contenido, base_dir)
        except Exception as name:
            QtGui.QMessageBox.critical(self.main, "Error", str(name))

    def _obtener_ruta_al_ejemplo(self, categoria, nombre):
        recurso = "../ejemplos/ejemplos/" + categoria + "/" + nombre + ".py"
        return pilas.utils.obtener_ruta_al_recurso(recurso)

    def _cuando_termina_la_ejecucion_del_ejemplo(self, codigo=0, estado=0):
        "Vuelve a permitir que se usen todos los botone de la interfaz."
        salida = str(self.process.readAll())

        if codigo and salida:
            QtGui.QMessageBox.critical(self.main, "Error al iniciar ejemplo", "Error: \n" + salida)

    def _cuando_selecciona_interprete(self):
        if sys.platform == "darwin":
        	QtCore.QTimer.singleShot(500, self._iniciar_interprete_diferido)
        else:
            if sys.platform == "win32":
                self._ejecutar_comando(sys.executable, ['-i'], '.')
            else:
                self._ejecutar_comando(sys.executable, [sys.argv[0], '-i'], '.')


    def _iniciar_interprete_diferido(self):
        self.instancia_interprete = pilas.interprete.main(self.main, True)

    def ejecutar_script(self, nombre_archivo_script, directorio_trabajo):
        self.nombre_archivo_script = nombre_archivo_script
        self.directorio_trabajo = directorio_trabajo

        if sys.platform == "darwin":
            pilas.interprete.cargar_ejemplo(self.main, True, nombre_archivo_script)
        else:
            try:
                self._ejecutar_comando(sys.executable, [nombre_archivo_script], directorio_trabajo)
            except Exception as e:
                QtGui.QMessageBox.critical(self.main, "Error", str(e))

    def _ejecutar_comando(self, comando, argumentos, directorio_trabajo):
        "Ejecuta un comando en segundo plano."

        if os.path.exists(argumentos[0]):
            self.observar_cambios_de_archivos(argumentos[0], directorio_trabajo)

        self.process = QtCore.QProcess(self.main)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.finished.connect(self._cuando_termina_la_ejecucion_del_ejemplo)
        self.process.setWorkingDirectory(directorio_trabajo)
        self.process.start(comando, argumentos)
        self.process.waitForStarted()

    def observar_cambios_de_archivos(self, nombre_archivo_script, directorio_trabajo):
        for f in self.watcher.files():
            self.watcher.removePath(f)

        self.watcher.addPath(nombre_archivo_script)
        #(nombre_archivo_script, directorio_trabajo))

    def _reiniciar_proceso(self):
        nombre_archivo_script = self.nombre_archivo_script
        if nombre_archivo_script:
            directorio_trabajo = self.directorio_trabajo
            self.process.terminate()
            self.process.waitForFinished(3000)
            self._ejecutar_comando(sys.executable, [nombre_archivo_script], directorio_trabajo)

    def _cuando_selecciona_abrir_manual(self):
        pilas.manual.main(self.main, True)
        
    def _cuando_selecciona_abrir_tutoriales(self):
        pilas.tutoriales.main(self.main, True)

    def _consultar(self, parent, titulo, mensaje):
        "Realizar una consulta usando un cuadro de dialogo."
        return QtGui.QMessageBox.question(parent, titulo, mensaje,
                                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    def salir(self, *_):
        self.main.close()

    def evaluar_javascript(self, codigo):
        self.webView.page().mainFrame().evaluateJavaScript(codigo)

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAcceptDrops(True)

    def definir_receptor_de_comandos(self, ui):
        self.ui = ui

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.ui.evaluar_javascript("resaltar_caja_destino_para_soltar(true);")

    def dragLeaveEvent(self, event):
        self.ui.evaluar_javascript("resaltar_caja_destino_para_soltar(false);")

    def dragMoveEvent(self, event):
        super(MainWindow, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                archivo = url.toLocalFile()
                path = os.path.dirname(str(archivo))

                self.ui.ejecutar_script(archivo, path)
                event.acceptProposedAction()
        else:
            super(MainWindow,self).dropEvent(event)
        self.ui.evaluar_javascript("resaltar_caja_destino_para_soltar(false);")

    def closeEvent(self, event):
        # TODO: Evitar cerrar la aplicación de esta forma, el
        # problema se produce a causa del objeto widget de pilas. En
        # una situación normal, la este método no devería ser necesario, pyqt
        # tiene que cerrar la aplicación cuando la última ventana se cierra.
        QtGui.qApp.closeAllWindows()
        import sys
        sys.exit(0)

def ejecutar():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("pilas-engine")

    main = MainWindow()
    ui = VentanaAsistente()
    ui.setupUi(main)
    main.definir_receptor_de_comandos(ui)

    main.show()
    main.raise_()
    app.exec_()
