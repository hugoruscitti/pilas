# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

BRACES = {'(':')', '[':']', '{':'}'}
COMILLAS = {'"':'"', "'":"'"}
CHARACTERS = {}
for d in (BRACES, COMILLAS): CHARACTERS.update(d)


class DictionaryCompleter(QtGui.QCompleter):

    def __init__(self, parent=None):
        QtGui.QCompleter.__init__(self, [], parent)

    def set_dictionary(self, words):
        model = QtGui.QStringListModel(words, self)
        self.setModel(model)


class CompletionTextEdit(QtGui.QTextEdit):

    def __init__(self, parent=None):
        super(CompletionTextEdit, self).__init__(parent)
        self.completer = None
        self.moveCursor(QtGui.QTextCursor.End)
        self.dictionary = DictionaryCompleter()
        self.set_completer(self.dictionary)
        self.set_dictionary([])

    def set_dictionary(self, list):
        self.dictionary.set_dictionary(list)
        self.set_completer(self.dictionary)
        self.setFocus()

    def set_completer(self, completer):
        completer.setWidget(self)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.connect(self.completer, QtCore.SIGNAL("activated(const QString&)"), self.insert_completation)

    def insert_completation(self, completion):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        tc.removeSelectedText()

        if str(completion).endswith('('):
            tc.insertText(completion[:-1])
        else:
            tc.insertText(completion)

        self.setTextCursor(tc)
        self.clearFocus()
        self.setFocus()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)

    def autocomplete(self, event):
        if not self.interpreterLocals['pilas'].configuracion.autocompletado_habilitado():
            return

        # Completar comillas y braces
        if event.key() in [Qt.Key_QuoteDbl, Qt.Key_Apostrophe]:
            self._autocompletar_comillas(event.text())

        elif event.key() in [Qt.Key_ParenLeft, Qt.Key_BraceLeft,
                             Qt.Key_BracketLeft]:
            self._autocompletar_braces(event.text())

        current_char = event.text()
        word = self._get_current_word() + current_char
        is_shift_pressed = (event.modifiers() & QtCore.Qt.ShiftModifier)

        if not event.text() and not is_shift_pressed:
            self.completer.popup().hide()
            return False

        if self.completer and self.completer.popup().isVisible():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Escape):
                event.ignore()
                return True
            elif event.text() in ['(', ')', '?']:
                self.completer.popup().hide()
                return False
            elif event.key() in (QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Space):
                self.completer.popup().hide()
                return False

        if is_shift_pressed:
            return

        codigo_completo = unicode(self._get_current_line() + event.text())
        values = self.funcion_valores_autocompletado(codigo_completo)

        if unicode(word).endswith('.'):
            word = ''

        # Evita todos los metodos privados si no se escribe un _
        values = [v for v in values if not v.startswith('_')]

        if '__builtins__' in values:
            values.remove('__builtins__')

        self.set_dictionary(values)
        self.completer.setCompletionPrefix(word)

        if values:
            #self.completer.completionCount() > -1:

            popup = self.completer.popup()
            popup.setStyleSheet("border: 1px solid gray")
            popup.setFont(self.font())
            popup.setCurrentIndex(self.completer.completionModel().index(0,0))

            if self.completer and not self.completer.popup().isVisible():
                cr = self.cursorRect()
                column_width = self.completer.popup().sizeHintForColumn(0)
                scroll_width = self.completer.popup().verticalScrollBar().sizeHint().width()
                cr.setWidth(column_width + scroll_width)
                self.completer.complete(cr)
        else:
            self.completer.popup().hide()

    def _autocompletar_comillas(self, comilla):
        tc = self.textCursor()
        tc.insertText(comilla)
        tc.setPosition(tc.position()-1)
        self.setTextCursor(tc)

    def _autocompletar_braces(self, brace):
        tc = self.textCursor()
        tc.insertText(BRACES[str(brace)])
        tc.setPosition(tc.position()-1)
        self.setTextCursor(tc)

    def _eliminar_pares_de_caracteres(self):
        tc = self.textCursor()
        line = self._get_current_line()
        position = self._get_position_in_block()
        if position < len(line) - 1:
            char = unicode(line[position])
            nextchar = unicode(line[position+1])
            if char in CHARACTERS and nextchar in CHARACTERS.values():
                tc.deleteChar()

    def funcion_valores_autocompletado(self, texto):
        "Retorna una lista de valores propuestos para autocompletar"
        scope = self.interpreterLocals
        texto = texto.replace('(', ' ').split(' ')[-1]

        if '.' in texto:
            palabras = texto.split('.')
            ultima = palabras.pop()
            prefijo = '.'.join(palabras)

            try:
                items = eval("[(x, callable(getattr(eval('%s'), x))) for x in dir(%s)]" %(prefijo, prefijo), scope)

                elementos = [x+'(' if invocable else x for (x, invocable) in items]
            except:
                # TODO: notificar este error de autocompletado en algun lado...
                return []

            resultados = [a for a in elementos if a.lower().startswith(ultima.lower())]
        else:
            resultados = [a for a in scope.keys() if a.lower().startswith(texto.lower())]

        return resultados
