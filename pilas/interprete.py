# -*- coding: utf-8 -*-
import sys

try:
    from PyQt4 import QtCore, QtGui
    from interprete_base import Ui_InterpreteDialog
except:
    print "ERROR: No se encuentra pyqt"
    Ui_InterpreteDialog = object
    pass

import pilas
import utils

try:
    sys.path.append(utils.obtener_ruta_al_recurso('../lanas'))
except IOError, e:
    pass

try:
    import lanas
except ImportError, e:
    print e


import os

if os.environ.has_key('lanas'):
    del os.environ['lanas']

class VentanaInterprete(Ui_InterpreteDialog):

    def setupUi(self, main):
        self.main = main
        Ui_InterpreteDialog.setupUi(self, main)
        scope = self._insertar_ventana_principal_de_pilas()
        self._insertar_consola_interactiva(scope)
        pilas.utils.centrar_ventana(main)

        # Haciendo que el panel de pilas y el interprete no se puedan
        # ocultar completamente.
        self.splitter_vertical.setCollapsible(1, False)

        self.colapsar_ayuda()
        self.cargar_ayuda()

        # Observa el deslizador vertical para mostrar el boton de ayuda
        # pulsado o despulsado.
        self.splitter_vertical.connect(self.splitter_vertical, QtCore.SIGNAL("splitterMoved(int, int)"), self.cuando_mueve_deslizador)

        self.manual_button.connect(self.manual_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_ayuda)

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
        
        self.navegador.history().setMaximumItemCount(0)

    def colapsar_ayuda(self):
        self.splitter_vertical.setSizes([0])
        self.manual_button.setChecked(False)

    def cargar_ayuda(self):
        file_path = utils.obtener_ruta_al_recurso('manual/index.html')
        file_path = os.path.abspath(file_path)

        archivo = open(file_path, "rt")
        contenido = archivo.read().decode('utf8')
        archivo.close()

        base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        self.navegador.setHtml(contenido, base_dir)

    def definir_icono(self, boton, ruta):
        icon = QtGui.QIcon();
        icon.addFile(pilas.utils.obtener_ruta_al_recurso(ruta), QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        boton.setIcon(icon)
        boton.setText('')

    def cuando_mueve_deslizador(self, a1, a2):
        self.manual_button.setChecked(a1 != 0)

    def cuando_pulsa_el_boton_ayuda(self):
        if self.manual_button.isChecked():
            self.splitter_vertical.setSizes([300])
        else:
            self.splitter_vertical.setSizes([0])

    def pulsa_boton_depuracion(self):
        pilas.atajos.definir_modos(
                            info=self.pushButton_6.isChecked(),              # F07
                            puntos_de_control=self.pushButton_5.isChecked(), # F08
                            radios=self.pushButton_4.isChecked(),            # F09
                            areas=self.pushButton_3.isChecked(),             # F10
                            fisica=self.pushButton_2.isChecked(),
                            posiciones=self.pushButton.isChecked(),
                )

    def raw_input(self, mensaje):
        text, state = QtGui.QInputDialog.getText(self, "raw_input", mensaje)
        return str(text)

    def input(self, mensaje):
        text, state = QtGui.QInputDialog.getText(self, "raw_input", mensaje)
        return eval(str(text))

    def help(self, objeto=None):
        if objeto:
            print help(objeto)
        else:
            print "Escribe help(objeto) para obtener ayuda sobre ese objeto."

    def _insertar_ventana_principal_de_pilas(self):
        pilas.iniciar(usar_motor='qtsugargl', ancho=640, alto=400)

        mono = pilas.actores.Mono()

        ventana = pilas.mundo.motor.ventana
        canvas = pilas.mundo.motor.canvas
        canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()

        self.canvas.addWidget(ventana)
        self.canvas.setCurrentWidget(ventana)
        return {'pilas': pilas, 'mono': mono, 'self': self}

    def _insertar_consola_interactiva(self, scope):
        codigo_inicial = [
                'import pilas',
                '',
                'pilas.iniciar()',
                'mono = pilas.actores.Mono()',
                ]

        consola = lanas.interprete.Ventana(self.splitter, scope, "\n".join(codigo_inicial))
        self.console.addWidget(consola)
        self.console.setCurrentWidget(consola)

def main(parent=None, do_raise=False):
    dialog = QtGui.QDialog(parent)
    dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)
    ui = VentanaInterprete()
    ui.setupUi(dialog)

    if do_raise:
        dialog.show()
        dialog.raise_()

    dialog.exec_()
