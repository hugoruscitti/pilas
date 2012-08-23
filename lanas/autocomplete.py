from PyQt4 import QtGui, QtCore

min_show = 2

class DictionaryCompleter(QtGui.QCompleter):
    def __init__(self, parent=None):
        self.words = []
        QtGui.QCompleter.__init__(self, self.words, parent)

    def append(self,list):
        self.words=self.words+list
        fix=[]
        for word in self.words:
            if not word in fix:
                fix.append(word)
        self.words=fix

        QtGui.QCompleter.__init__(self, self.words, parent=None)

class CompletionTextEdit(QtGui.QTextEdit):

    def __init__(self, parent=None):
        super(CompletionTextEdit, self).__init__(parent)
        self.completer = None
        self.moveCursor(QtGui.QTextCursor.End)
        self.dictionary = DictionaryCompleter()
        self.setCompleter(self.dictionary)
        self.Update_dictionary(["Nueva palabra"])

    def Update_dictionary(self,list):
        self.dictionary.append(list)
        self.setCompleter(self.dictionary)
        self.setFocus()

    def setCompleter(self, completer):
        completer.setWidget(self)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.connect(self.completer, QtCore.SIGNAL("activated(const QString&)"), self.insertCompletion)


    def insertCompletion(self, completion):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        tc.removeSelectedText()
        tc.insertText(completion)
        self.setTextCursor(tc)

        self.clearFocus()
        self.setFocus()

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)

    def autocomplete(self, event):

        if self.completer and self.completer.popup().isVisible():
            if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Escape, QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab):
                event.ignore()
                return True

        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Space)

        if (not self.completer or not isShortcut):
            return

        ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier , QtCore.Qt.ShiftModifier)

        if ctrlOrShift and event.text().isEmpty():
            # ctrl or shift key on it's own
            return

        eow = QtCore.QString("~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=L")

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                        not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        if (not isShortcut and (hasModifier or event.text().isEmpty() or completionPrefix.length() < min_show or eow.contains(event.text().right(1)))):
            self.completer.popup().hide()
            return False

        if (completionPrefix != self.completer.completionPrefix()):
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0,0))
            return

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)
