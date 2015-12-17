# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import codecs
import os
import time
import sys

from PyQt4.QtGui import (QKeySequence, QIcon, QLabel)
from PyQt4 import QtCore

import lanas
import pilasengine
from pilasengine.interprete import editor
from pilasengine.interprete.interprete_base import Ui_InterpreteWindow

class VentanaInterprete(Ui_InterpreteWindow):

    def setupUi(self, main):
        self.main = main
        Ui_InterpreteWindow.setupUi(self, main)
        main.closeEvent = self.on_close_event
        self.iniciar_interfaz()
        self._vincular_atajos_de_teclado()
        self.editor.crear_archivo_inicial()

    def _vincular_atajos_de_teclado(self):
        self.pushButton_6.setShortcut(QKeySequence('F7'))
        self.pushButton_5.setShortcut(QKeySequence('F8'))
        self.pushButton_3.setShortcut(QKeySequence('F10'))
        self.pushButton_2.setShortcut(QKeySequence('F11'))
        self.pushButton.setShortcut(QKeySequence('F12'))

    def iniciar_interfaz(self):
        self.scope = self._iniciar_pilas()
        self.crear_mensaje_cargando()

        self._insertar_consola_interactiva()
        self._insertar_editor(self.consola)

        self.definir_fuente_desde_configuracion()

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
        self._conectar_observadores_splitters()

    def on_close_event(self, evento):
        if not self.editor.salir():
            evento.ignore()
            return

        evento.accept()

        self.scope['pilas'].cerrar()

    def _conectar_botones(self):
        # Botón del editor
        self.definir_icono(self.editor_button, 'iconos/editor.png')
        self.editor_button.connect(self.editor_button,
                                   QtCore.SIGNAL("clicked()"),
                                   self.cuando_pulsa_el_boton_editor)


        # Botón del manual
        self.definir_icono(self.manual_button, 'iconos/manual.png')
        self.manual_button.connect(self.manual_button,
                                   QtCore.SIGNAL("clicked()"),
                                   self.cuando_pulsa_el_boton_manual)

        # Botón del interprete
        self.definir_icono(self.interprete_button, 'iconos/interprete.png')
        self.interprete_button.connect(self.interprete_button,
                                       QtCore.SIGNAL("clicked()"),
                                       self.cuando_pulsa_el_boton_interprete)

        # Botón guardar del interprete
        self.definir_icono(self.guardar_button, 'iconos/guardar.png')
        self.interprete_button.connect(self.guardar_button,
                                       QtCore.SIGNAL("clicked()"),
                                       self.cuando_pulsa_el_boton_guardar_interprete)

        # Botón configuración
        self.definir_icono(self.configuracion_button, 'iconos/preferencias.png')
        self.interprete_button.connect(self.configuracion_button,
                                       QtCore.SIGNAL("clicked()"),
                                       self.cuando_pulsa_el_boton_configuracion)
        # Botón para limpiar el intérprete
        self.definir_icono(self.limpiar_button, 'iconos/limpiar.png')
        self.limpiar_button.connect(self.limpiar_button,
                                    QtCore.SIGNAL("clicked()"),
                                    self.cuando_pulsa_el_boton_limpiar)

        # Botón para pasar a modo pantalla completa.
        if sys.platform == 'darwin':
            self.pantalla_completa_button.enabled = True
        else:
            self.pantalla_completa_button.enabled = False
            self.pantalla_completa_button.setToolTip("Pasa al modo pantalla completa (deshabilitado en windows / linux por el momento).")


        self.definir_icono(self.pantalla_completa_button, 'iconos/pantalla_completa.png')
        self.pantalla_completa_button.connect(self.pantalla_completa_button,
                                    QtCore.SIGNAL("clicked()"),
                                    self.cuando_pulsa_el_boton_pantalla_completa)

        # F7 Modo informacion de sistema
        self.definir_icono(self.pushButton_6, 'iconos/f07.png')
        self.pushButton_6.connect(self.pushButton_6,
                                  QtCore.SIGNAL("clicked()"),
                                  self.pulsa_boton_depuracion)

        # F8 Modo puntos de control
        self.definir_icono(self.pushButton_5, 'iconos/f08.png')
        self.pushButton_5.connect(self.pushButton_5,
                                  QtCore.SIGNAL("clicked()"),
                                  self.pulsa_boton_depuracion)


        # F10 Modo areas de colision
        self.definir_icono(self.pushButton_3, 'iconos/f10.png')
        self.pushButton_3.connect(self.pushButton_3,
                                  QtCore.SIGNAL("clicked()"),
                                  self.pulsa_boton_depuracion)

        # F11 Modo fisica
        self.definir_icono(self.pushButton_2, 'iconos/f11.png')
        self.pushButton_2.connect(self.pushButton_2,
                                  QtCore.SIGNAL("clicked()"),
                                  self.pulsa_boton_depuracion)

        # F12 Modo depuracion de posicion
        self.definir_icono(self.pushButton, 'iconos/f12.png')
        self.pushButton.connect(self.pushButton,
                                QtCore.SIGNAL("clicked()"),
                                self.pulsa_boton_depuracion)

    def _conectar_observadores_splitters(self):
        # Observa los deslizadores para mostrar mostrar los botones de ayuda o consola activados.
        self.splitter_vertical.connect(self.splitter_vertical,
                                       QtCore.SIGNAL("splitterMoved(int, int)"),
                                       self.cuando_mueve_deslizador_vertical)

        self.splitter.connect(self.splitter,
                              QtCore.SIGNAL("splitterMoved(int, int)"),
                              self.cuando_mueve_deslizador)

        self.splitter_editor.connect(self.splitter_editor,
                                     QtCore.SIGNAL("splitterMoved(int, int)"),
                                     self.cuando_mueve_deslizador_del_editor)

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
        base_dir = QtCore.QUrl.fromLocalFile(file_path)
        self.navegador.load(base_dir)

    def definir_icono(self, boton, ruta):
        icon = QIcon()
        archivo = pilasengine.utils.obtener_ruta_al_recurso(ruta)
        icon.addFile(archivo, QtCore.QSize(), QIcon.Normal, QIcon.Off)
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
            self.mostrar_editor()
        else:
            self.ocultar_editor()

    def mostrar_editor(self):
        self.splitter_editor.setSizes([300, 250])
        self.editor_button.setChecked(True)

    def ocultar_editor(self):
        self.splitter_editor.setSizes([500, 0])
        self.editor_button.setChecked(False)

    def cuando_pulsa_el_boton_interprete(self):
        if self.interprete_button.isChecked():
            self.mostrar_el_interprete()
        else:
            self.ocultar_el_interprete()

    def ocultar_el_interprete(self):
        self.colapsar_interprete()

    def mostrar_el_interprete(self):
        self.splitter.setSizes([300, 100])
        self.interprete_button.setChecked(True)

    def pulsa_boton_depuracion(self):
        pilas = self.scope['pilas']
        pilas.depurador.definir_modos(
            info=self.pushButton_6.isChecked(),               # F07
            puntos_de_control=self.pushButton_5.isChecked(),  # F08
            radios=False,                                     # F09
            areas=self.pushButton_3.isChecked(),              # F10
            fisica=self.pushButton_2.isChecked(),             # F11
            posiciones=self.pushButton.isChecked(),           # F12
        )

    def _iniciar_pilas(self):
        pilas = pilasengine.iniciar(640, 400)
        pilas.definir_iniciado_desde_asistente(True)

        scope = {'pilas': pilas,
                 'self': self,
                 'colores': pilasengine.colores,
                 'pilasengine': pilasengine}

        self.canvas.addWidget(scope['pilas'].widget)

        return scope

    def crear_mensaje_cargando(self):
        self.cargando = QLabel("Cargando ...")
        self.cargando.setAlignment(QtCore.Qt.AlignHCenter |
                                   QtCore.Qt.AlignVCenter)
        self.canvas.addWidget(self.cargando)
        self.cargando.setStyleSheet("background-color: 'black'; color:#FFFFFF")

    def mostrar_mensaje_cargando(self):
        self.canvas.setCurrentWidget(self.cargando)

    def insertar_widget_de_pilas(self):
        self.scope['pilas'].widget.setFocusPolicy(QtCore.Qt.ClickFocus)

        # Se asegura de mostrar la ventana de pilas luego de 1/2 segundo.
        if getattr(self, 'stimer', None):
            self.stimer.stop()
            self.stimer.deleteLater()

        self.stimer = QtCore.QTimer()
        self.stimer.timeout.connect(self._mostrar_widget_de_pilas)
        self.stimer.setSingleShot(True)
        self.stimer.start(300)

    def _mostrar_widget_de_pilas(self):
        self.canvas.setCurrentWidget(self.scope['pilas'].widget)
	self.scope['pilas'].widget.setFocus(QtCore.Qt.ActiveWindowFocusReason)


    def _insertar_editor(self, consola_lanas):
        self.widget_editor = editor.WidgetEditor(self.main, self.scope, consola_lanas, self)
        self.editor_layout.addWidget(self.widget_editor)
        self.editor = self.widget_editor.editor
        self.editor.signal_ejecutando.connect(self.actualizar_widget_pilas)

    def _insertar_consola_interactiva(self):
        codigo_inicial = u'''import pilasengine
                            pilas = pilasengine.iniciar()
                            mono = pilas.actores.Mono()'''

        widgetlanas = lanas.WidgetLanas(self.splitter, self.scope, codigo_inicial)
        self.console.addWidget(widgetlanas)
        self.console.setCurrentWidget(widgetlanas)
        self.consola = widgetlanas.lanas

    def definir_fuente_desde_configuracion(self):
        fuente = pilasengine.configuracion.Configuracion().obtener_fuente()
        self.editor.definir_fuente(fuente)
        self.widget_editor.definir_fuente(fuente)
        self.consola.definir_fuente(fuente)

    def cuando_pulsa_el_boton_guardar_interprete(self):
        self.consola.guardar_contenido_con_dialogo()

    def cuando_pulsa_el_boton_configuracion(self):
        pilasengine.abrir_configuracion()
        self.definir_fuente_desde_configuracion()

    def cuando_pulsa_el_boton_limpiar(self):
        self.consola.limpiar()

    def cuando_pulsa_el_boton_pantalla_completa(self):
        self.scope['pilas'].widget.definir_modo_pantalla_completa()

    def _reiniciar_y_ejecutar(self, archivo):
        self.watcher.removePath(archivo)
        self.watcher.addPath(archivo)

        # Evita actualizar el archivo si no han pasado mas de 3 segundos.
        if time.time() - self.watcher_ultima_invocacion < 3:
            return

        self.watcher_ultima_invocacion = time.time()

        self._cargar_codigo_del_editor_desde_archivo(archivo)
        f = codecs.open(unicode(archivo), 'r', 'utf-8')
        contenido = f.read()

        # Cambia el directorio para que los recursos del directorio
        # del archivo a ejecutar se puedan cargar correctamente.
        current_path = os.path.dirname(archivo)

        self.ejecutar_codigo_como_string(contenido, current_path)
        f.close()

    def actualizar_widget_pilas(self):
        self.mostrar_mensaje_cargando()
        self.insertar_widget_de_pilas()

        # Evita perder los ejes del modo de depuracion 'posiciones'
        self.scope['pilas'].depurador.definir_modos()
        self.pulsa_boton_depuracion()
