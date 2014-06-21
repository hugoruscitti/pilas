# -*- coding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
import sys
import re
import codecs
import time

from PyQt4 import QtCore, QtGui

import pilasengine
from pilasengine.interprete.interprete_base import Ui_InterpreteWindow
from pilasengine import lanas
import editor
from pilasengine import utils


class VentanaInterprete(Ui_InterpreteWindow):

    def setupUi(self, main):
        self.main = main
        Ui_InterpreteWindow.setupUi(self, main)
        main.closeEvent = self.on_close_event
        self.iniciar_interfaz()
        self._vincular_atajos_de_teclado()
        self.editor.ejecutar()

    def _vincular_atajos_de_teclado(self):
        QtGui.QShortcut(QtGui.QKeySequence("F5"), self.main, self.cuando_pulsa_el_boton_ejecutar)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+r"), self.main, self.cuando_pulsa_el_boton_ejecutar)

        self.pushButton_6.setShortcut(QtGui.QKeySequence('F7'))
        self.pushButton_5.setShortcut(QtGui.QKeySequence('F8'))
        self.pushButton_4.setShortcut(QtGui.QKeySequence('F9'))
        self.pushButton_3.setShortcut(QtGui.QKeySequence('F10'))
        self.pushButton_2.setShortcut(QtGui.QKeySequence('F11'))
        self.pushButton.setShortcut(QtGui.QKeySequence('F12'))

        # Solo en MacOS informa que la tecla Command sustituye a CTRL.
        if sys.platform == 'darwin':
            self.boton_ejecutar.setToolTip(u"Ejecutar el código actual (F5 o ⌘R)")

    def iniciar_interfaz(self):
        self.scope = self._insertar_ventana_principal_de_pilas()
        self._insertar_consola_interactiva(self.scope)
        self._insertar_editor(self.consola.obtener_fuente(), self.scope)

        # Haciendo que el panel de pilas y el interprete no se puedan
        # ocultar completamente.
        self.splitter_vertical.setCollapsible(1, False)
        self.splitter.setCollapsible(0, False)

        # Define el tamaño inicial de la consola.
        self.splitter.setSizes([300, 100])

        self.colapsar_ayuda()
        self.colapsar_editor()
        self.cargar_ayuda()
        self.navegador.history().setMaximumItemCount(0)

        self._conectar_botones()
        self._conectar_botones_del_editor()
        self._conectar_observadores_splitters()

    def consultar_si_quiere_perder_cambios(self):
        titulo = u"¿Quieres salir?"
        aviso = u"Se perderán los cambios sin guardar... ¿Quieres perder los cambios del editor realmente?"
        return self._consultar(self.main, titulo, aviso)

    def on_close_event(self, evento):

        if not self.editor.tiene_cambios_sin_guardar():
            evento.accept()
            return

        consulta = self.consultar_si_quiere_perder_cambios()

        if consulta:
            evento.accept()
        else:
            evento.ignore()

    def _consultar(self, parent, titulo, mensaje):
        """Realizar una consulta usando un cuadro de dialogo simple.

        Este método retorna True si el usuario acepta la pregunta."""
        # TODO: reemplazar por un dialogo que no tenga los botones YES NO, sino algo en español: http://stackoverflow.com/questions/15682665/how-to-add-custom-button-to-a-qmessagebox-in-pyqt4
        respuesta = QtGui.QMessageBox.question(parent, titulo, mensaje,
                                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        return (respuesta == QtGui.QMessageBox.Yes)

    def _conectar_botones(self):
        # Botón del editor
        self.definir_icono(self.editor_button, 'iconos/editor.png')
        self.editor_button.connect(self.editor_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_editor)

        # Botón del manual
        self.definir_icono(self.manual_button, 'iconos/manual.png')
        self.manual_button.connect(self.manual_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_manual)

        # Botón del interprete
        self.definir_icono(self.interprete_button, 'iconos/interprete.png')
        self.interprete_button.connect(self.interprete_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_interprete)

        # Botón del guardar
        self.definir_icono(self.boton_guardar, 'iconos/guardar.png')
        self.boton_guardar.connect(self.boton_guardar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_guardar)

        self.definir_icono(self.boton_ejecutar, 'iconos/ejecutar.png')
        #self.interprete_button.connect(self.boton_guardar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_guardar)

        self.definir_icono(self.boton_abrir, 'iconos/abrir.png')
        self.boton_abrir.connect(self.boton_abrir, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_abrir)

        # Botón del guardar
        self.definir_icono(self.guardar_button, 'iconos/guardar.png')
        self.interprete_button.connect(self.guardar_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_guardar)

        # F7 Modo informacion de sistema
        self.definir_icono(self.pushButton_6, 'iconos/f07.png')
        self.pushButton_6.connect(self.pushButton_6, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F8 Modo puntos de control
        self.definir_icono(self.pushButton_5, 'iconos/f08.png')
        self.pushButton_5.connect(self.pushButton_5, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F9 Modo radios de colision
        self.definir_icono(self.pushButton_4, 'iconos/f09.png')
        self.pushButton_4.connect(self.pushButton_4, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F10 Modo areas de colision
        self.definir_icono(self.pushButton_3, 'iconos/f10.png')
        self.pushButton_3.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F11 Modo fisica
        self.definir_icono(self.pushButton_2, 'iconos/f11.png')
        self.pushButton_2.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F12 Modo depuracion de posicion
        self.definir_icono(self.pushButton, 'iconos/f12.png')
        self.pushButton.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

    def _conectar_botones_del_editor(self):
        self.boton_ejecutar.connect(self.boton_ejecutar, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_ejecutar)

    def _conectar_observadores_splitters(self):
        # Observa los deslizadores para mostrar mostrar los botones de ayuda o consola activados.
        self.splitter_vertical.connect(self.splitter_vertical, QtCore.SIGNAL("splitterMoved(int, int)"), self.cuando_mueve_deslizador_vertical)
        self.splitter.connect(self.splitter, QtCore.SIGNAL("splitterMoved(int, int)"), self.cuando_mueve_deslizador)
        self.splitter_editor.connect(self.splitter_editor, QtCore.SIGNAL("splitterMoved(int, int)"), self.cuando_mueve_deslizador_del_editor)

    def colapsar_ayuda(self):
        self.splitter_vertical.setSizes([0])
        self.manual_button.setChecked(False)

    def colapsar_editor(self):
        self.splitter_editor.setSizes([0])
        self.editor_button.setChecked(False)

    def colapsar_interprete(self):
        self.splitter.setSizes([300, 0])
        self.interprete_button.setChecked(False)

    def cargar_ayuda(self):
        file_path = pilasengine.utils.obtener_ruta_al_recurso('manual/index.html')
        file_path = os.path.abspath(file_path)
        base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        self.navegador.load(base_dir)

    def definir_icono(self, boton, ruta):
        icon = QtGui.QIcon()
        archivo = pilasengine.utils.obtener_ruta_al_recurso(ruta)
        icon.addFile(archivo, QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        boton.setIcon(icon)
        boton.setText('')

    def cuando_mueve_deslizador_vertical(self, a1, a2):
        self.manual_button.setChecked(a1 != 0)

    def cuando_mueve_deslizador_del_editor(self, a1, a2):
        area = self.splitter_editor.sizes()[1]
        self.editor_button.setChecked(area != 0)

    def cuando_mueve_deslizador(self, a1, a2):
        altura_interprete = self.splitter.sizes()[1]
        self.interprete_button.setChecked(altura_interprete != 0)

    def cuando_pulsa_el_boton_manual(self):
        if self.manual_button.isChecked():
            self.splitter_vertical.setSizes([300])
        else:
            self.splitter_vertical.setSizes([0])

    def cuando_pulsa_el_boton_editor(self):
        if self.editor_button.isChecked():
            self.splitter_editor.setSizes([300, 250])
        else:
            self.splitter_editor.setSizes([500, 0])

    def cuando_pulsa_el_boton_interprete(self):
        if self.interprete_button.isChecked():
            self.splitter.setSizes([300, 100])
        else:
            self.splitter.setSizes([300, 0])

    def cuando_pulsa_el_boton_ejecutar(self):
        self.editor.ejecutar()

    def pulsa_boton_depuracion(self):
        pilas = self.scope['pilas']
        pilas.depurador.definir_modos(
                            info=self.pushButton_6.isChecked(),              # F07
                            puntos_de_control=self.pushButton_5.isChecked(), # F08
                            radios=self.pushButton_4.isChecked(),            # F09
                            areas=self.pushButton_3.isChecked(),             # F10
                            fisica=self.pushButton_2.isChecked(),            # F11
                            posiciones=self.pushButton.isChecked(),          # F12
                )

    def raw_input(self, mensaje):
        text, _ = QtGui.QInputDialog.getText(self.main, "raw_input", mensaje)
        return str(text)

    def input(self, mensaje):
        text, _ = QtGui.QInputDialog.getText(self.main, "raw_input", mensaje)
        return eval(str(text))

    def help(self, objeto=None):
        if objeto:
            print help(objeto)
        else:
            print "Escribe help(objeto) para obtener ayuda sobre ese objeto."

    def _insertar_ventana_principal_de_pilas(self):
        pilas = pilasengine.iniciar(640, 400)
        pilas.definir_iniciado_desde_asistente(True)

        scope = {'pilas': pilas,
                 'self': self,
                 'colores': pilasengine.colores,
                 'pilasengine': pilasengine
                 }
        ventana = pilas.obtener_widget()

        self.cargando = QtGui.QLabel("Cargando ...")
        self.cargando.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.canvas.addWidget(self.cargando)
        self.canvas.setCurrentWidget(self.cargando)

        self.ventana_pilas = ventana

        self.stimer = QtCore.QTimer()

        return scope

    def mostrar_mensaje_cargando(self):
        self.canvas.setCurrentWidget(self.cargando)

    def reinsertar_widget_de_pilas(self, widget):
        widget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.ventana_pilas = widget
        self.canvas.setFocus()
        self.canvas.addWidget(widget)

        # Se asegura de mostrar la ventana de pilas luego de 1/2 segundo.
        if getattr(self, 'stimer', None):
            self.stimer.stop()
            self.stimer.deleteLater()

        self.stimer = QtCore.QTimer()
        self.stimer.timeout.connect(self._mostrar_ventana_de_pilas)
        self.stimer.setSingleShot(True)
        self.stimer.start(300)

    def _mostrar_ventana_de_pilas(self):
        self.canvas.setCurrentWidget(self.ventana_pilas)

    def _insertar_editor(self, fuente, scope):
        componente = editor.Editor(self.main, scope, self)
        componente.definir_fuente(fuente)
        self.editor_placeholder.addWidget(componente)
        self.editor_placeholder.setCurrentWidget(componente)
        self.editor = componente
        self._cargar_resaltador_de_sintaxis()

    def _cargar_resaltador_de_sintaxis(self):
        self._highlighter = lanas.highlighter.Highlighter(self.editor.document(), 'python', lanas.highlighter.COLOR_SCHEME)

    def _insertar_consola_interactiva(self, scope):
        codigo_inicial = [
                'import pilasengine',
                '',
                'pilas = pilasengine.iniciar()',
                'mono = pilas.actores.Mono()',
        ]

        consola = lanas.ventana.Ventana(self.splitter, scope, "\n".join(codigo_inicial))
        self.console.addWidget(consola)
        self.console.setCurrentWidget(consola)
        self.consola = consola
        self.consola.text_edit.setFocus()


    def cuando_pulsa_el_boton_abrir(self):
        self.editor.abrir_con_dialogo()

    def cuando_pulsa_el_boton_guardar(self):
        self.editor.guardar_con_dialogo()

    def ejecutar_y_reiniciar_si_cambia(self, archivo):
        self.watcher_ultima_invocacion = time.time() - 500
        self.watcher = QtCore.QFileSystemWatcher(parent=self.main)
        self.watcher.connect(self.watcher, QtCore.SIGNAL('fileChanged(const QString&)'), self._reiniciar_y_ejecutar)
        self.watcher.addPath(archivo)
        self._reiniciar_y_ejecutar(archivo)
        self._cargar_codigo_del_editor_desde_archivo(archivo)

    def _cargar_codigo_del_editor_desde_archivo(self, archivo):
        self.editor.cargar_desde_archivo(archivo)

    def _reiniciar_y_ejecutar(self, archivo):
        self.watcher.removePath(archivo)
        self.watcher.addPath(archivo)

        # Evita actualizar el archivo si no han pasado mas de 3 segundos.
        if time.time() - self.watcher_ultima_invocacion < 3:
            return

        self.watcher_ultima_invocacion = time.time();

        self._cargar_codigo_del_editor_desde_archivo(archivo)
        f = codecs.open(unicode(archivo), 'r', 'utf-8')
        contenido = f.read()

        # Cambia el directorio para que los recursos del directorio
        # del archivo a ejecutar se puedan cargar correctamente.
        current_path = os.path.dirname(archivo)
        os.chdir(current_path)

        self.ejecutar_codigo_como_string(contenido)
        f.close()

    def ejecutar_codigo_como_string(self, contenido):
        contenido = re.sub('coding\s*:\s*', '', contenido)      # elimina cabecera de encoding.
        contenido = contenido.replace('import pilasengine', '')
        contenido = contenido.replace('pilas = pilasengine.iniciar', 'pilas.reiniciar')

        self.consola.ejecutar(contenido)
        scope_nuevo = self.consola.obtener_scope()
        self.editor.actualizar_scope(scope_nuevo)
        widget = scope_nuevo['pilas'].widget
        self.mostrar_mensaje_cargando()
        self.reinsertar_widget_de_pilas(widget)


def abrir():
    MainWindow = QtGui.QMainWindow()

    ui = VentanaInterprete()
    ui.setupUi(MainWindow)

    utils.centrar_ventana(MainWindow)
    MainWindow.show()
    MainWindow.raise_()

    return MainWindow

def abrir_script_con_livereload(archivo):
    MainWindow = QtGui.QMainWindow()

    ui = VentanaInterprete()
    ui.setupUi(MainWindow)

    utils.centrar_ventana(MainWindow)
    MainWindow.show()
    MainWindow.raise_()
    ui.ejecutar_y_reiniciar_si_cambia(archivo)

    ui.colapsar_interprete()
    return MainWindow