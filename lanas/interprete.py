import re
import code
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import highlighter
import autocomplete

class DictionaryCompleter(QCompleter):

    def __init__(self, parent=None):
        QCompleter.__init__(self, [], parent)
        self.popup().setFont(QFont('Monaco', 20))
        self.set_words(["uno", "dos", "tres"])

    def set_words(self, words):
        self.model().setStringList(words)


class Ventana(QWidget):

    def __init__(self, parent):

        super(Ventana, self).__init__(parent)
        hBox = QHBoxLayout()

        self.setLayout(hBox)
        self.textEdit = PyInterp(self)

        # this is how you pass in locals to the interpreter
        self.textEdit.initInterpreter(locals())

        self.resize(650, 300)
        self.centerOnScreen()

        hBox.addWidget(self.textEdit)
        hBox.setMargin(0)
        hBox.setSpacing(0)
        self.raise_()

    def centerOnScreen(self):
        # center the widget on the screen
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width()  / 2) - (self.frameSize().width()  / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

class PyInterp(autocomplete.CompletionTextEdit):

    class InteractiveInterpreter(code.InteractiveInterpreter):

        def __init__(self, locals):
            code.InteractiveInterpreter.__init__(self, locals)

        def runIt(self, command):
            code.InteractiveInterpreter.runsource(self, command)


    def __init__(self,  parent):
        super(PyInterp,  self).__init__(parent)

        sys.stdout = self
        sys.stderr = self
        self.refreshMarker = False # to change back to >>> from ...
        self.multiLine = False # code spans more than one line
        self.command = ''    # command to be ran
        self.marker()                   # make the >>> or ... marker
        self.history = []    # list of commands entered
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

        # initilize interpreter with self locals
        self.initInterpreter(locals())

    def _set_font_size(self, font_size):
        self.font_size = font_size
        self.setFont(QFont('Monaco', font_size))

    def _change_font_size(self, delta_size):
        self._set_font_size(self.font_size + delta_size)

    def marker(self):
        if self.multiLine:
            self.insertPlainText(u'... ')
        else:
            self.insertPlainText(u'>>> ')

    def initInterpreter(self, interpreterLocals=None):
        if interpreterLocals:
            # when we pass in locals, we don't want it to be named "self"
            # so we rename it with the name of the class that did the passing
            # and reinsert the locals back into the interpreter dictionary
            selfName = interpreterLocals['self'].__class__.__name__
            interpreterLocalVars = interpreterLocals.pop('self')
            self.interpreterLocals[selfName] = interpreterLocalVars
        else:
            self.interpreterLocals = interpreterLocals
        self.interpreter = self.InteractiveInterpreter(self.interpreterLocals)

    def updateInterpreterLocals(self, newLocals):
        className = newLocals.__class__.__name__
        self.interpreterLocals[className] = newLocals

    def write(self, line):
        self.insertPlainText(line)
        self.ensureCursorVisible()

    def clearCurrentBlock(self):
        # block being current row
        length = len(self.document().lastBlock().text()[4:])
        if length == 0:
            return None
        else:
            # should have a better way of doing this but I can't find it
            [self.textCursor().deletePreviousChar() for x in xrange(length)]
        return True

    def recallHistory(self):
        # used when using the arrow keys to scroll through history
        self.clearCurrentBlock()
        if self.historyIndex <> -1:
            self.insertPlainText(self.history[self.historyIndex])
        return True

    def customCommands(self, command):

        if command == '!hist': # display history
            self.append('') # move down one line
            # vars that are in the command are prefixed with ____CC and deleted
            # once the command is done so they don't show up in dir()
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

        if re.match('!hist\(\d+\)', command): # recall command from history
            backup = self.interpreterLocals.copy()
            history = self.history[:]
            history.reverse()
            index = int(command[6:-1])
            self.clearCurrentBlock()
            command = history[index]
            if command[-1] == ':':
                self.multiLine = True
            self.write(command)
            self.updateInterpreterLocals(backup)
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

        if event.key() == Qt.Key_Tab:
            word = self._get_current_word()
            block = self._get_current_block_prefix()

            """
            if block != word:
                items = eval('dir(%s)' %block, self.interpreterLocals, {})
            else:
                items = self.interpreterLocals

            opciones = [o for o in items if o.startswith(word)]

            if opciones:
                self._set_current_word(opciones[0])

            event.ignore()
            return

            """
            if (word != self.completer.completionPrefix()):
                self.completer.setCompletionPrefix(word)
                popup = self.completer.popup()
                popup.setCurrentIndex(self.completer.completionModel().index(0,0))

                cr = self.cursorRect()
                cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())

                self.completer.complete(cr)
                event.ignore()

        if event.modifiers() & Qt.AltModifier:
            if event.key() == Qt.Key_Minus:
                self._change_font_size(-2)
                event.ignore()
                return
            elif event.key() == Qt.Key_Equal:
                self._change_font_size(+2)
                event.ignore()
                return

        if event.key() == Qt.Key_Down:
            if self.historyIndex == len(self.history):
                self.historyIndex -= 1
            try:
                if self.historyIndex > -1:
                    self.historyIndex -= 1
                    self.recallHistory()
                else:
                    self.clearCurrentBlock()
            except:
                pass
            return None

        if event.key() == Qt.Key_Up:
            try:
                if len(self.history) - 1 > self.historyIndex:
                    self.historyIndex += 1
                    self.recallHistory()
                else:
                    self.historyIndex = len(self.history)
            except:
                pass
            return None

        if event.key() == Qt.Key_Home:
            # set cursor to position 4 in current block. 4 because that's where
            # the marker stops
            blockLength = len(self.document().lastBlock().text()[4:])
            lineLength  = len(self.document().toPlainText())
            position = lineLength - blockLength
            textCursor  = self.textCursor()
            textCursor.setPosition(position)
            self.setTextCursor(textCursor)
            return None

        if event.key() in [Qt.Key_Left, Qt.Key_Backspace]:
            # don't allow deletion of marker
            if self.textCursor().positionInBlock() == 4:
                return None

        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            line = self._get_entered_line()
            self.historyIndex = -1

            if self.customCommands(line):
                return None
            else:
                try:
                    line[-1]
                    self.haveLine = True
                    if line[-1] == ':':
                        self.multiLine = True
                    self.history.insert(0, line)
                except:
                    self.haveLine = False

                if self.haveLine and self.multiLine: # multi line command
                    self.command += line + '\n' # + command and line
                    self.append('') # move down one line
                    self.marker() # handle marker style
                    return None

                if self.haveLine and not self.multiLine: # one line command
                    self.command = line # line is the command
                    self.append('') # move down one line
                    self.interpreter.runIt(self.command)
                    self.command = '' # clear command
                    self.marker() # handle marker style
                    return None

                if self.multiLine and not self.haveLine: #  multi line done
                    self.append('') # move down one line
                    self.interpreter.runIt(self.command)
                    self.command = '' # clear command
                    self.multiLine = False # back to single line
                    self.marker() # handle marker style
                    return None

                if not self.haveLine and not self.multiLine:  # just enter
                    self.append('')
                    self.marker()
                    return None
                return None

        # allow all other key events
        super(PyInterp, self).keyPressEvent(event)
