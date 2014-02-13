import sys
import os

from PyQt4 import QtGui, QtCore

def autocompletar(scope, texto):
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
        tc.insertText(completion)
        self.setTextCursor(tc)
        self.clearFocus()
        self.setFocus()

    def _get_current_word(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def _get_current_line(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.LineUnderCursor)
        return tc.selectedText()[2:]

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)

    def autocomplete(self, event):
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

        codigo_completo = str(self._get_current_line() + event.text())
        values = autocompletar(self.interpreterLocals, codigo_completo)

        if str(word).endswith('.'):
            word = ''

        # Evita todos los metodos privados si no se escribe un _
        values = [v for v in values if not v.startswith('_')]

        # Previene que pilas autocomplete nombre de modulos en los actores.
        # (solo mostrara el nombre de las clases).
        if codigo_completo.startswith('pilas.actores.'):
            values = [v for v in values if v.istitle()]

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
