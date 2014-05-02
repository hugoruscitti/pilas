import sys
import os

from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QTextCursor

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

    def _get_current_line(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.LineUnderCursor)
        return tc.selectedText()[2:]

    def _get_current_word(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def _cambiar_sentencia_con_deslizador(self, nueva):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.LineUnderCursor)
        texto = tc.selectedText()

        palabras = texto.split(' ')
        numero = None

        # Busca cuales de las palabras es el numero a reemplazar.
        for p in palabras:
            if unicode(p).lstrip("-+").isdigit():
                numero = p

        texto = texto.replace(numero, str(nueva))
        tc.removeSelectedText()

        tc.insertText(texto)
        self.setTextCursor(tc)

        linea = str(self._get_current_line())
        exec(linea, self.interpreterLocals)

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)

    def mousePressEvent(self, *args, **kwargs):
        retorno = QtGui.QTextEdit.mousePressEvent(self, *args, **kwargs)
        linea = self._get_current_line()
        palabra = self._get_current_word()

        # Si parece una sentencia se asignacion normal permie cambiarla con un deslizador.
        if '=' in str(linea) and str(palabra).isdigit():
            self.mostrar_deslizador()

        return retorno

    def mostrar_deslizador(self):
        valor_inicial = self._get_current_word()
        self.deslizador = Deslizador(self, self.textCursor(), valor_inicial, self._cambiar_sentencia_con_deslizador)
        self.deslizador.show()

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

class Deslizador(QtGui.QWidget):

    def __init__(self, parent, cursor, valor_inicial, funcion_cuando_cambia):
        QtGui.QWidget.__init__(self, parent)
        self.funcion_cuando_cambia = funcion_cuando_cambia

        layout = QtGui.QGridLayout(self)
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.valueChanged[int].connect(self.on_change)
        slider.setValue(int(valor_inicial))
        slider.setMaximum(300)
        slider.setMinimum(-300)
        slider.setMinimumWidth(200)

        layout.addWidget(slider)
        layout.setContentsMargins(7, 7, 7, 7)

        self.setLayout(layout)
        self.adjustSize()

        self.setWindowFlags(QtCore.Qt.Popup)

        point = parent.cursorRect(cursor).bottomRight()
        global_point = parent.mapToGlobal(point)

        self.move(global_point)

    def on_change(self, valor):
        self.funcion_cuando_cambia(str(valor))