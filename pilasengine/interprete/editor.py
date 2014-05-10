from PyQt4 import QtGui
from PyQt4 import QtCore

CONTENIDO = """import pilasengine

pilas = pilasengine.iniciar()

aceituna = pilas.actores.Aceituna()
aceituna.escala = [2]

pilas.ejecutar()"""

class Editor(QtGui.QTextEdit):

    def __init__(self):
        QtGui.QTextEdit.__init__(self)
        self.insertPlainText(CONTENIDO)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            tc = self.textCursor()
            tc.insertText("    ")
        else:
            return QtGui.QTextEdit.keyPressEvent(self, event)

    def definir_fuente(self, fuente):
        self.setFont(fuente)