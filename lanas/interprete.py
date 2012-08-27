import code
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import highlighter
import autocomplete

class Ventana(QWidget):

    def __init__(self, parent, title):
        super(Ventana, self).__init__(parent)
        self.setWindowTitle(title)
        box = QHBoxLayout()
        box.setMargin(12)
        box.setSpacing(0)

        self.setLayout(box)

        self.text_edit = InterpreteTextEdit(self)
        self.text_edit.init(locals())

        self.resize(650, 300)
        self.center_on_screen()

        box.addWidget(self.text_edit)
        self.raise_()

    def center_on_screen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width()  / 2) - (self.frameSize().width()  / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def closeEvent(self, event):
        autocomplete.stop_daemon()
        import sys
        sys.exit(0)

class InterpreteTextEdit(autocomplete.CompletionTextEdit):

    def __init__(self,  parent):
        super(InterpreteTextEdit,  self).__init__(parent)

        sys.stdout = self
        sys.stderr = self
        self.refreshMarker = False
        self.multiline = False
        self.command = ''
        self.marker()        # cursor >>> o ...
        self.history = []
        self.historyIndex = -1
        self.interpreterLocals = {}

        # setting the color for bg and text
        #palette = QPalette()
        #palette.setColor(QPalette.Base, QColor(0, 0, 0))
        #palette.setColor(QPalette.Text, QColor(0, 255, 0))
        #self.setPalette(palette)

        self._set_font_size(20)
        self._highlighter = highlighter.Highlighter(self.document(), 'python', highlighter.COLOR_SCHEME)

        ##completer = DictionaryCompleter()
        ##self._set_completer(completer)


    def _set_font_size(self, font_size):
        self.font_size = font_size
        font = QFont('Monaco', font_size)
        self.setFont(font)

    def _change_font_size(self, delta_size):
        self._set_font_size(self.font_size + delta_size)

    def marker(self):
        if self.multiline:
            self.insertPlainText(u'... ')
        else:
            self.insertPlainText(u'>>> ')

    def init(self, interpreter_locals):
        if interpreter_locals:
            self.interpreter = code.InteractiveInterpreter(interpreter_locals)

    def updateInterpreterLocals(self, newLocals):
        className = newLocals.__class__.__name__
        self.interpreterLocals[className] = newLocals

    def write(self, line):
        self.insertPlainText(line)
        self.ensureCursorVisible()

    def clearCurrentBlock(self):
        length = len(self.document().lastBlock().text()[4:])

        if length:
            [self.textCursor().deletePreviousChar() for x in xrange(length)]

    def recall_history(self):
        self.clearCurrentBlock()
        if self.historyIndex <> -1:
            self.insertPlainText(self.history[self.historyIndex])

    def custom_commands(self, command):

        if command == '!hist':
            self.append('')
            backup = self.interpreterLocals.copy()
            history = self.history[:]
            history.reverse()
            for i, x in enumerate(history):
                iSize = len(str(i))
                delta = len(str(len(history))) - iSize
                line = line  = ' ' * delta + '%i: %s' % (i, x) + '\n'
                self.write(line)
            self.updateInterpreterLocals(backup)
            self.marker()
            return True

        return False

    def _get_entered_line(self):
        # set cursor to end of line to avoid line splitting
        textCursor = self.textCursor()
        position   = len(self.document().toPlainText())
        textCursor.setPosition(position)
        self.setTextCursor(textCursor)

        line = str(self.document().lastBlock().text())[4:] # remove marker
        line.rstrip()
        return line

    def _get_current_word(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def _get_current_block_prefix(self):
        tc = self.textCursor()
        tc.select(QTextCursor.BlockUnderCursor)
        current_block = tc.selectedText()
        words = current_block.split(" ")
        prefix = words[-1]

        if '(' in prefix:
            prefix = prefix.split('(')[-1]

        if '.' in prefix:
            prefixes = prefix.split('.')
            prefixes = prefixes[:-1]
            return '.'.join([str(s) for s in prefixes])
        else:
            return prefix

    def _set_current_word(self, word):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        tc.removeSelectedText()
        tc.insertText(word)

    def keyPressEvent(self, event):

        """
        if event.key() == Qt.Key_Tab:
            word = self._get_current_word()
            block = self._get_current_block_prefix()

            if block != word:
                items = eval('dir(%s)' %block, self.interpreterLocals, {})
            else:
                items = self.interpreterLocals

            opciones = [o for o in items if o.startswith(word)]

            if opciones:
                self._set_current_word(opciones[0])

            event.ignore()
            return

            if (word != self.completer.completionPrefix()):
                self.completer.setCompletionPrefix(word)
                popup = self.completer.popup()
                popup.setCurrentIndex(self.completer.completionModel().index(0,0))

                cr = self.cursorRect()
                cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())

                self.completer.complete(cr)
                event.ignore()
        """

        # cambia el tamano de la tipografia.
        if event.modifiers() & Qt.AltModifier:
            if event.key() == Qt.Key_Minus:
                self._change_font_size(-2)
                event.ignore()
                return
            elif event.key() == Qt.Key_Equal:
                self._change_font_size(+2)
                event.ignore()
                return

        # navegar por el historial
        if event.key() == Qt.Key_Down:
            if self.historyIndex == len(self.history):
                self.historyIndex -= 1
            try:
                if self.historyIndex > -1:
                    self.historyIndex -= 1
                    self.recall_history()
                else:
                    self.clearCurrentBlock()
            except:
                pass
            return None

        # navegar por el historial
        if event.key() == Qt.Key_Up:
            try:
                if len(self.history) - 1 > self.historyIndex:
                    self.historyIndex += 1
                    self.recall_history()
                else:
                    self.historyIndex = len(self.history)
            except:
                pass
            return None

        # ir al primer caracter del interprete cuando pulsa HOME
        if event.key() == Qt.Key_Home:
            blockLength = len(self.document().lastBlock().text()[4:])
            lineLength  = len(self.document().toPlainText())
            position = lineLength - blockLength
            textCursor  = self.textCursor()
            textCursor.setPosition(position)
            self.setTextCursor(textCursor)
            return None

        if event.key() in [Qt.Key_Left, Qt.Key_Backspace]:
            if self.textCursor().positionInBlock() < 5:
                return None

        if self.autocomplete(event):
            return None

        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            line = self._get_entered_line()
            self.historyIndex = -1

            if not self.custom_commands(line):
                try:
                    line[-1]
                    self.haveLine = True
                    if line[-1] == ':':
                        self.multiline = True
                    self.history.insert(0, line)
                except:
                    self.haveLine = False

                if self.haveLine and self.multiline: # multi line command
                    self.command += line + '\n' # + command and line
                    self.append('')
                    self.marker() # handle marker style
                    return None

                if self.haveLine and not self.multiline: # one line command
                    self.command = line # line is the command
                    self.append('') # move down one line
                    self.interpreter.runsource(self.command)
                    self.command = '' # clear command
                    self.marker() # handle marker style
                    return None

                if self.multiline and not self.haveLine: #  multi line done
                    self.append('') # move down one line
                    self.interpreter.runsource(self.command)
                    self.command = '' # clear command
                    self.multiline = False # back to single line
                    self.marker() # handle marker style
                    return None

                if not self.haveLine and not self.multiline:  # just enter
                    self.append('')
                    self.marker()
                    return None

                return None

        super(InterpreteTextEdit, self).keyPressEvent(event)
