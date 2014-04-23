# -*- encoding: utf-8 -*-
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

    def iniciar_con_ventana(self, ventana):
        self.manual = None
        self.interprete = None
        self.ventana = ventana

    @QtCore.pyqtSlot()
    def abrir_interprete(self):
        if not self.interprete:
            self.interprete = pilasengine.abrir_interprete()
        else:
            self.interprete.show()
            self.interprete.raise_()

    @QtCore.pyqtSlot()
    def abrir_manual(self):
        if not self.manual:
            self.manual = pilasengine.abrir_manual()
        else:
            self.manual.show()
            self.manual.raise_()

    @QtCore.pyqtSlot()
    def abrir_sitio_de_pilas(self):
        webbrowser.open("http://www.pilas-engine.com.ar")

class VentanaAsistente(Base):

    def __init__(self):
        Base.__init__(self)

    def setupUi(self, MainWindow):
        Base.setupUi(self, MainWindow)

        self.interlocutor = Interlocutor()
        self.interlocutor.iniciar_con_ventana(self)

        self.webView.page().mainFrame().javaScriptWindowObjectCleared.connect(
                self.populateJavaScriptWindowObject)

        self._cargar_pagina_principal()
        self._habilitar_inspector_web()

        #self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateExternalLinks)
        #self.webView.connect(self.webView, QtCore.SIGNAL("linkClicked(const QUrl&)"), self.cuando_pulsa_link)

    def populateJavaScriptWindowObject(self):
        self.webView.page().mainFrame().addToJavaScriptWindowObject("interlocutor", self.interlocutor)

    def test(self):
        self.webView.setAcceptDrops(False)
        self._deshabilitar_barras_de_scroll()
        #self.statusbar.showMessage(u"Versión " + pilas.version())
        self.salir_action.connect(self.salir_action, QtCore.SIGNAL("triggered()"), self.salir)
        #self._consultar_ultima_version_del_servidor()
        #self.watcher = QtCore.QFileSystemWatcher(parent=self.main)
        #self.watcher.connect(self.watcher, QtCore.SIGNAL('fileChanged(const QString&)'), self._reiniciar_proceso)
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
        file_path = pilasengine.utils.obtener_ruta_al_recurso('asistente/index.html')
        self.webView.load(QtCore.QUrl.fromLocalFile(file_path))

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
                    print accion, "sobre el ejemplo", ejemplo
            else:
                raise Exception(seccion + "es una opcion desconocida")

    def _obtener_ruta_al_ejemplo(self, categoria, nombre):
        recurso = "../ejemplos/ejemplos/" + categoria + "/" + nombre + ".py"
        return pilasengine.utils.obtener_ruta_al_recurso(recurso)

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
            except Exception, e:
                QtGui.QMessageBox.critical(self.main, "Error", str(e))

    def observar_cambios_de_archivos(self, nombre_archivo_script, directorio_trabajo):
        for f in self.watcher.files():
            self.watcher.removePath(f)

        self.watcher.addPath(nombre_archivo_script)
        #(nombre_archivo_script, directorio_trabajo))

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

    def definir_receptor_de_comandos(self, ui):
        self.ui = ui

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.ui.evaluar_javascript("resaltar_caja_destino_para_soltar(true);")

    def dragLeaveEvent(self, event):
        self.ui.evaluar_javascript("resaltar_caja_destino_para_soltar(false);")

    def dragMoveEvent(self, event):
        super(VentanaAsistente, self).dragMoveEvent(event)

    def linkClicked(self, arg__1):
        print "ASDADASD"

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
        # ura situación normal, la este método no devería ser necesario, pyqt
        # tiene que cerrar la aplicación cuando la última ventana se cierra.
        QtGui.qApp.closeAllWindows()
        import sys
        sys.exit(0)

def abrir():
    MainWindow = QtGui.QMainWindow()

    ui = VentanaAsistente()
    ui.setupUi(MainWindow)

    MainWindow.show()
    MainWindow.raise_()

    pilasengine.utils.verificar_si_lanas_existe(MainWindow)

    return MainWindow