# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit

from interprete_base import Ui_InterpreteWindow
import pilas
import utils

sys.path.append('../')

import lanas


class VentanaInterprete(Ui_InterpreteWindow):

    def setupUi(self, main):
        self.main = main
        Ui_InterpreteWindow.setupUi(self, main)

        scope = self._insertar_ventana_principal_de_pilas()
        self._insertar_consola_interactiva(scope)

    def _insertar_ventana_principal_de_pilas(self):
        pilas.iniciar(usar_motor='qtsugargl')
        mono = pilas.actores.Mono()
        mono.aprender(pilas.habilidades.Arrastrable)
        canvas = pilas.mundo.motor.widget
        canvas.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.canvas.addWidget(canvas)
        self.canvas.setCurrentWidget(canvas)
        return {'pilas':pilas, 'mono':mono}

    def _insertar_consola_interactiva(self, scope):
        consola = lanas.interprete.Ventana(self.splitter, scope)
        consola.text_edit.write("import pilas")
        self.console.addWidget(consola)
        self.console.setCurrentWidget(consola)

def main(parent=None):
    main = QtGui.QMainWindow(parent)
    ui = VentanaInterprete()
    ui.setupUi(main)

    main.show()
    main.raise_()
