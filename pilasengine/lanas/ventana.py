# -*- encoding: utf-8 -*-
import code
import sys
import inspect

import os
os.environ['lanas'] = 'enabled'

from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import highlighter
import autocomplete
import interprete_textedit




class Ventana(QWidget):

    def __init__(self, parent=None, scope=None, codigo_inicial=""):
        super(Ventana, self).__init__(parent)
        box = QVBoxLayout()
        box.setMargin(0)
        box.setSpacing(0)

        self.setLayout(box)

        if not scope:
            scope = locals()

        if not 'inspect' in scope:
            scope['inspect'] = inspect

        self.text_edit = interprete_textedit.InterpreteTextEdit(self, codigo_inicial)
        self.text_edit.init(scope)

        self.tip_widget = QLabel(self)
        self.tip_widget.setText("")

        box.addWidget(self.text_edit)
        box.addWidget(self.tip_widget)

        self.resize(650, 300)
        self.center_on_screen()
        self.raise_()

    def obtener_fuente(self):
        return self.text_edit.font()

    def ejecutar(self, codigo):
        """Ejecuta el codigo en formato string enviado."""
        exec(codigo, self.text_edit.interpreterLocals)

    def obtener_scope(self):
        return self.text_edit.interpreterLocals

    def center_on_screen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width()  / 2) - (self.frameSize().width()  / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def closeEvent(self, event):
        sys.exit(0)

    def alternar_log(self):
        if self.log_widget.isHidden():
            self.log_widget.show()
        else:
            self.log_widget.hide()

    def raw_input(self, mensaje):
        text, state = QInputDialog.getText(self, "raw_input", mensaje)
        return str(text)

    def input(self, mensaje):
        text, state = QInputDialog.getText(self, "raw_input", mensaje)
        return eval(str(text))

    def help(self, objeto=None):
        if objeto:
            print help(objeto)
        else:
            print "Escribe help(objeto) para obtener ayuda sobre ese objeto."
