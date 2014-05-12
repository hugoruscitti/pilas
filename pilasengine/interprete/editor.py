# -*- encoding: utf-8 -*-
import codecs

from PyQt4 import QtGui
from PyQt4 import QtCore

from pilasengine.lanas import autocomplete
from pilasengine.lanas import editor_con_deslizador

CONTENIDO = """import pilasengine

pilas = pilasengine.iniciar()

aceituna = pilas.actores.Aceituna()
aceituna.escala = [2]

pilas.ejecutar()"""

class Editor(autocomplete.CompletionTextEdit, editor_con_deslizador.EditorConDeslizador):

    def __init__(self, interpreterLocals):
        autocomplete.CompletionTextEdit.__init__(self, None, self.funcion_valores_autocompletado)
        self.interpreterLocals = interpreterLocals
        self.insertPlainText(CONTENIDO)
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            tc = self.textCursor()
            tc.insertText("    ")
        else:
            if self.autocomplete(event):
                return None

            return QtGui.QTextEdit.keyPressEvent(self, event)

    def definir_fuente(self, fuente):
        self.setFont(fuente)

    def actualizar_scope(self, scope):
        self.interpreterLocals = scope

    def funcion_valores_autocompletado(self, texto):
        scope = self.interpreterLocals
        texto = texto.replace('(', ' ').split(' ')[-1]

        if '.' in texto:
            palabras = texto.split('.')
            ultima = palabras.pop()
            prefijo = '.'.join(palabras)

            try:
                elementos = eval("dir(%s)" %prefijo, scope)
            except:
                # TODO: notificar este error de autocompletado en algun lado...
                return []

            return [a for a in elementos if a.startswith(ultima)]
        else:
            return [a for a in scope.keys() if a.startswith(texto)]

    def _get_current_line(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.LineUnderCursor)
        return tc.selectedText()

    def cargar_desde_archivo(self, ruta):
        archivo = codecs.open(unicode(ruta), 'r', 'utf-8')
        contenido = archivo.read()
        archivo.close()
        self.setText(contenido)