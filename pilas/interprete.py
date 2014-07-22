# -*- coding: utf-8 -*-
import sys
import inspect

try:
    from PyQt4 import QtCore, QtGui
    from .interprete_base import Ui_InterpreteWindow
except:
    print("ERROR: No se encuentra pyqt")
    Ui_InterpreteWindow = object
    pass

import pilas
from . import utils

try:
    sys.path.append(utils.obtener_ruta_al_recurso('../lanas'))
except IOError as e:
    pass

try:
    import lanas
except ImportError as e:
    print(e)


import os

if 'lanas' in os.environ:
    del os.environ['lanas']

class VentanaInterprete(Ui_InterpreteWindow):

    def setupUi(self, main, ejecutar_codigo_inicial=False):
        self.main = main
        Ui_InterpreteWindow.setupUi(self, main)
        scope = self._insertar_ventana_principal_de_pilas(ejecutar_codigo_inicial)
        self._insertar_consola_interactiva(scope, ejecutar_codigo_inicial)
        pilas.utils.centrar_ventana(main)

        # Haciendo que el panel de pilas y el interprete no se puedan
        # ocultar completamente.
        self.splitter_vertical.setCollapsible(1, False)
        self.splitter.setCollapsible(0, False)

        # Define el tamaño inicial de la consola.
        self.splitter.setSizes([300, 100])

        self.colapsar_ayuda()
        self.cargar_ayuda()
        self.navegador.history().setMaximumItemCount(0)

        self._conectar_botones()
        self._conectar_observadores_splitters()

    def _conectar_botones(self):
        # Botón del manual
        self.definir_icono(self.manual_button, 'iconos/manual.png')
        self.manual_button.connect(self.manual_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_manual)

        # Botón del interprete
        self.definir_icono(self.interprete_button, 'iconos/interprete.png')
        self.interprete_button.connect(self.interprete_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_interprete)

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

    def _conectar_observadores_splitters(self):
        # Observa los deslizadores para mostrar mostrar los botones de ayuda o consola activados.
        self.splitter_vertical.connect(self.splitter_vertical, QtCore.SIGNAL("splitterMoved(int, int)"), self.cuando_mueve_deslizador_vertical)
        self.splitter.connect(self.splitter, QtCore.SIGNAL("splitterMoved(int, int)"), self.cuando_mueve_deslizador)

    def colapsar_ayuda(self):
        self.splitter_vertical.setSizes([0])
        self.manual_button.setChecked(False)

    def cargar_ayuda(self):
        file_path = utils.obtener_ruta_al_recurso('manual/index.html')
        file_path = os.path.abspath(file_path)
        base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        self.navegador.load(base_dir)

    def definir_icono(self, boton, ruta):
        icon = QtGui.QIcon();
        icon.addFile(pilas.utils.obtener_ruta_al_recurso(ruta), QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        boton.setIcon(icon)
        boton.setText('')

    def cuando_mueve_deslizador_vertical(self, a1, a2):
        self.manual_button.setChecked(a1 != 0)

    def cuando_mueve_deslizador(self, a1, a2):
        altura_interprete = self.splitter.sizes()[1]
        self.interprete_button.setChecked(altura_interprete != 0)

    def cuando_pulsa_el_boton_manual(self):
        if self.manual_button.isChecked():
            self.splitter_vertical.setSizes([300])
        else:
            self.splitter_vertical.setSizes([0])

    def cuando_pulsa_el_boton_interprete(self):
        if self.interprete_button.isChecked():
            self.splitter.setSizes([300, 100])
        else:
            self.splitter.setSizes([300, 0])

    def pulsa_boton_depuracion(self):
        pilas.atajos.definir_modos(
                            info=self.pushButton_6.isChecked(),              # F07
                            puntos_de_control=self.pushButton_5.isChecked(), # F08
                            radios=self.pushButton_4.isChecked(),            # F09
                            areas=self.pushButton_3.isChecked(),             # F10
                            fisica=self.pushButton_2.isChecked(),            # F11
                            posiciones=self.pushButton.isChecked(),          # F12
                )

    def raw_input(self, mensaje):
        text, state = QtGui.QInputDialog.getText(self, "raw_input", mensaje)
        return str(text)

    def input(self, mensaje):
        text, state = QtGui.QInputDialog.getText(self, "raw_input", mensaje)
        return eval(str(text))

    def help(self, objeto=None):
        if objeto:
            print(help(objeto))
        else:
            print("Escribe help(objeto) para obtener ayuda sobre ese objeto.")

    def _insertar_ventana_principal_de_pilas(self, ejecutar_codigo_inicial):

        if pilas.esta_inicializada():
            pilas.reiniciar()

        pilas.iniciar(usar_motor='qtsugargl', ancho=640, alto=400)

        if ejecutar_codigo_inicial:
            from pilas.actores.robot import wait
            b = pilas.actores.Board("/dev/tty/USB0")
            r = pilas.actores.Robot(b, 1)
            scope = {'pilas': pilas, 'b': b, 'r': r, 'wait' : wait , 'self': self}
        else:
            scope = {'pilas': pilas, 'self': self}

        ventana = pilas.mundo.motor.ventana
        canvas = pilas.mundo.motor.canvas

        canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        self.canvas.addWidget(ventana)
        self.canvas.setCurrentWidget(ventana)
        return scope

    def _insertar_consola_interactiva(self, scope, ejecutar_codigo_inicial):
        if ejecutar_codigo_inicial:
            codigo_inicial = [
                'import pilas',
                '',
                'from pilas.actores.robot import wait',
                'pilas.iniciar()',
		'b = pilas.actores.Board("/dev/tty/USB0")',
		'r = pilas.actores.Robot(b, 1)',
                ]
        else:
            codigo_inicial = []
        
        try:
            consola = lanas.interprete.Ventana(self.splitter, scope, "\n".join(codigo_inicial))
        except:
            from lanas import lanas
            consola = lanas.interprete.Ventana(self.splitter, scope, "\n".join(codigo_inicial))
        
        self.console.addWidget(consola)
        self.console.setCurrentWidget(consola)
        self.consola = consola
        self.consola.text_edit.setFocus()

    def cuando_pulsa_el_boton_guardar(self):
        self.consola.text_edit.guardar_contenido_con_dialogo()

def cargar_ejemplo(parent=None, do_raise=False, ruta=None):
    main = QtGui.QMainWindow(parent)
    ui = VentanaInterprete()
    ui.setupUi(main, ejecutar_codigo_inicial=False)

    archivo = open(ruta, "rt")
    contenido = []
    for linea in archivo.readlines():
        if '#' in linea or 'path' in linea or 'import pilas' in linea or 'pilas.iniciar' in linea or 'pilas.ejecutar' in linea:
            pass
        else:
            contenido.append(linea)
    codigo = '\n'.join(contenido)

    ui.consola.ejecutar(codigo)

    archivo.close()

    #if sys.platform == 'darwin':
    #    if getattr(sys, 'frozen', None):
    #        main.showMinimized()
    #        main.showNormal()

    main.show()

    if do_raise:
        main.raise_()

    return main

def main(parent=None, do_raise=False):
    main = QtGui.QMainWindow(parent)
    ui = VentanaInterprete()
    ui.setupUi(main, ejecutar_codigo_inicial=True)

    #if sys.platform == 'darwin':
    #    if getattr(sys, 'frozen', None):
    #        main.showMinimized()
    #        main.showNormal()

    main.show()

    if do_raise:
        main.raise_()

    return main


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("pilas-engine")
    main()
    app.exec_()
