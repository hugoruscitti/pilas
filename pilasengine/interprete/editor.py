from PyQt4 import QtGui
from PyQt4 import QtCore

class Editor(QtGui.QTextEdit):

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            tc = self.textCursor()
            tc.insertText("    ")
        else:
            return QtGui.QTextEdit.keyPressEvent(self, event)

    def definir_fuente(self, fuente):
        self.setFont(fuente)