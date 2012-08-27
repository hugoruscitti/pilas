import sys
import os

# Hace que el directorio que esta mas arriba pueda
# tener modulos accesibles como por ejemplo kanzen.
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PATH, '..', 'kanzen'))

print sys.path

from PyQt4 import QtGui, QtCore
from kanzen import code_completion, completion_daemon

def stop_daemon():
    completion_daemon.shutdown_daemon()

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
        self.set_dictionary(["nueva_palabra", "import"])
        self.cc = code_completion.CodeCompletion()

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
        return tc.selectedText()[4:]

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)

    def autocomplete(self, event):
        word = self._get_current_word() + event.text()

        if not event.text() or event.text() == '.':
            self.completer.popup().hide()
            return False

        if self.completer and self.completer.popup().isVisible():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Escape):
                event.ignore()
                return True
            elif event.key() in (QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Space):
                self.completer.popup().hide()
                return False
        else:
            codigo = '\n'.join(self.history)
            self.cc.analyze_file('', codigo)

            codigo_completo = codigo + "\n" + self._get_current_line() + event.text()
            result = self.cc.get_completion(codigo_completo, len(codigo_completo))
            values = result['attributes'] + result.get('modules', []) + result['functions'] + result['classes']
            self.set_dictionary(values)

        if word != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(word)
            popup = self.completer.popup()
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
