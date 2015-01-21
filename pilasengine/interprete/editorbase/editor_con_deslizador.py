# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import re
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import deslizador

EXPRESION_SENTENCIA = r'.*\s*\=\s*(-*\d+\.*\d*)$'


class EditorConDeslizador(object):

    def _cambiar_sentencia_con_deslizador(self, nueva):
        try:
            linea = self._get_current_line()
            numero = self._obtener_numero_de_la_linea(linea)

            tc = self.textCursor()
            tc.select(QtGui.QTextCursor.LineUnderCursor)

            texto = tc.selectedText()
            texto = texto.replace(numero, str(nueva))
            tc.removeSelectedText()
            tc.insertText(texto)

            self.setTextCursor(tc)

            linea = str(self._get_current_line())
            exec(linea, self.interpreterLocals)
        except:
            pass

    def _obtener_numero_de_la_linea(self, linea):
        grupos =  re.search(EXPRESION_SENTENCIA, linea).groups()
        return grupos[0]

    def mousePressEvent(self, event):
        retorno = QtGui.QTextEdit.mousePressEvent(self, event)

        if event.button() == Qt.RightButton:
            pos = event.pos()
            cursor = self.cursorForPosition(pos)
            self.setTextCursor(cursor)

            linea = self._get_current_line()

            # Si parece una sentencia se asignacion normal permie cambiarla con un deslizador.
            try:
                if re.match(EXPRESION_SENTENCIA, str(linea)):
                    self.mostrar_deslizador()
            except UnicodeEncodeError:
                pass

        return retorno

    def _es_sentencia_asignacion_simple(self, linea):
        return re.match(EXPRESION_SENTENCIA, str(linea))

    def mostrar_deslizador(self):
        valor_inicial = self._obtener_numero_de_la_linea(self._get_current_line())
        self.deslizador = deslizador.Deslizador(self, self.textCursor(), valor_inicial, self._cambiar_sentencia_con_deslizador)
        self.deslizador.show()