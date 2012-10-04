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
    import lanas
except ImportError, e:
    print e
    pass


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
        pilas.utils.centrar_ventana(main)

    def _insertar_ventana_principal_de_pilas(self):
        pilas.iniciar(usar_motor='qtsugar', ancho=640, alto=400)

        mono = pilas.actores.Mono()

        ventana = pilas.mundo.motor.ventana
        canvas = pilas.mundo.motor.canvas
        canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()

        self.canvas.addWidget(ventana)
        self.canvas.setCurrentWidget(ventana)
        return {'pilas': pilas, 'mono': mono}

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
