# -*- coding: utf-8 -*-
from __future__ import absolute_import

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextFormat
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from pilas.console import console
from pilas.console import highlighter


INDENT = 4

EDITOR_STYLE = """QPlainTextEdit {
                    font-family: monospace;
                    font-size: 10;
                    color: black;
                    background-color: white;
                    selection-color: white;
                    selection-background-color: #437DCD;
                }"""


class ConsoleWidget(QPlainTextEdit):

    def __init__(self, locals):
        QPlainTextEdit.__init__(self, u'>>> ')
        self.setUndoRedoEnabled(False)
        self.setStyleSheet(EDITOR_STYLE)
        self.setToolTip(self.tr("Show/Hide (F4)"))

        self.prompt = u'>>> '
        self._console = console.Console(locals)
        self._history = []

        self._highlighter = highlighter.Highlighter(self.document(), 'python',
            highlighter.COLOR_SCHEME)

        self.connect(self, SIGNAL("cursorPositionChanged()"),
            self._highlight_current_line)
        self._highlight_current_line()

    def setCursorPosition(self, position):
        self.moveCursor(QTextCursor.StartOfLine)
        for i in xrange(len(self.prompt) + position):
            self.moveCursor(QTextCursor.Right)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self._write_command()
            return
        if self._get_cursor_position() < 0:
            self.setCursorPosition(0)
        if event.key() == Qt.Key_Tab:
            self.textCursor().insertText(' ' * INDENT)
            return
        if event.key() == Qt.Key_Home:
            self.setCursorPosition(0)
            return
        if event.key() == Qt.Key_PageUp:
            return
        elif event.key() in (Qt.Key_Left, Qt.Key_Backspace):
            if self._get_cursor_position() == 0:
                return
        elif event.key() == Qt.Key_Up:
            self._set_command(self._get_prev_history_entry())
            return
        elif event.key() == Qt.Key_Down:
            self._set_command(self._get_next_history_entry())
            return
        super(ConsoleWidget, self).keyPressEvent(event)

    def _add_prompt(self, incomplete):
        if incomplete:
            prompt = '.' * 3 + ' '
        else:
            prompt = self.prompt
        self.appendPlainText(prompt)
        self.moveCursor(QTextCursor.End)

    def _get_cursor_position(self):
        return self.textCursor().columnNumber() - len(self.prompt)

    def _write_command(self):
        command = self.document().findBlockByLineNumber(
                    self.document().lineCount() - 1).text()
        #remove the prompt from the QString
        command = command.remove(0, len(self.prompt)).toUtf8().data()
        self._add_history(command.decode('utf8'))
        incomplete = self._write(command.decode('utf8'))
        if not incomplete:
            output = self._read()
            if output is not None:
                if output.__class__.__name__ == 'unicode':
                    output = output.encode('utf8')
                self.appendPlainText(output.decode('utf8'))
        self._add_prompt(incomplete)

    def _set_command(self, command):
        self.moveCursor(QTextCursor.End)
        self.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        for i in xrange(len(self.prompt)):
            self.moveCursor(QTextCursor.Right, QTextCursor.KeepAnchor)
        self.textCursor().removeSelectedText()
        self.textCursor().insertText(command)
        self.moveCursor(QTextCursor.End)

    def _highlight_current_line(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.darkCyan)
            lineColor.setAlpha(20)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def mousePressEvent(self, event):
        #to avoid selection
        event.ignore()

    def _write(self, line):
        return self._console.push(line)

    def _read(self):
        return self._console.output

    def _add_history(self, command):
        if command and (not self._history or self._history[-1] != command):
            self._history.append(command)
        self.history_index = len(self._history)

    def _get_prev_history_entry(self):
        if self._history:
            self.history_index = max(0, self.history_index - 1)
            return self._history[self.history_index]
        return ''

    def _get_next_history_entry(self):
        if self._history:
            hist_len = len(self._history)
            self.history_index = min(hist_len, self.history_index + 1)
            if self.history_index < hist_len:
                return self._history[self.history_index]
        return ''
