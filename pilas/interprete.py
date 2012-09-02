# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit

from interprete_base import Ui_InterpreteDialog
import pilas
import utils

sys.path.append('../')

import lanas


class VentanaInterprete(Ui_InterpreteDialog):

    def setupUi(self, main):
        self.main = main
        Ui_InterpreteDialog.setupUi(self, main)

        scope = self._insertar_ventana_principal_de_pilas()
        self._insertar_consola_interactiva(scope)
        pilas.utils.centrar_ventana(main)
        pilas.utils.centrar_ventana(main)

    def _insertar_ventana_principal_de_pilas(self):
        pilas.iniciar(usar_motor='qtsugar')
        mono = pilas.actores.Mono()
        mono.aprender(pilas.habilidades.Arrastrable)
        canvas = pilas.mundo.motor.ventana
        canvas.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.canvas.addWidget(canvas)
        self.canvas.setCurrentWidget(canvas)
        return {'pilas': pilas, 'mono': mono}

    def _insertar_consola_interactiva(self, scope):
        consola = lanas.interprete.Ventana(self.splitter, scope)
        consola.text_edit.write("import pilas")
        self.console.addWidget(consola)
        self.console.setCurrentWidget(consola)

def main(parent=None):
    dialog = QtGui.QDialog(parent)
    dialog.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowContextHelpButtonHint)
    ui = VentanaInterprete()
    ui.setupUi(dialog)
    dialog.exec_()
