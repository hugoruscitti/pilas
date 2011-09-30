# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2011 - Diego Sarmentero
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
#
# module based in NINJA-IDE "locator.py" (http://ninja-ide.org)

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt


class ExampleLocatorWidget(QWidget):

    def __init__(self, data, parent):
        QWidget.__init__(self)
        self._parentTree = parent
        self.data = data

        hLocator = QHBoxLayout(self)
        hLocator.setContentsMargins(0, 0, 0, 0)
        self._completer = LocateCompleter(self)

        hLocator.addWidget(self._completer)

        self.connect(self._completer, SIGNAL("itemFound(QString)"),
            self.open_item)

    def setFocus(self):
        self._completer.setFocus()

    def open_item(self, path):
        self.emit(SIGNAL("itemFound(QString)"), path)


class LocateItem(QListWidgetItem):

    def __init__(self, name, path):
        QListWidgetItem.__init__(self, name)
        self.path = path


class LocateCompleter(QLineEdit):

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self._parent = parent

        try:
            self.setPlaceholderText("Buscar... (Ctrl+F)")
        except AttributeError:
            pass

        self.__prefix = ''
        self.frame = None
        self.tempLocations = []

        self.connect(self, SIGNAL("textChanged(QString)"),
            self.set_prefix)

    def set_prefix(self, prefix):
        self.__prefix = unicode(prefix.toLower())
        self._refresh_filter()

    def complete(self):
        self.frame = PopupCompleter(self.filter())
        self.frame.setFixedWidth(self._parent._parentTree.width())
        point = self._parent.mapToGlobal(self.pos())
        self.frame.show()
        self.frame.move(point.x(), point.y() - self.frame.height())

    def filter(self):
        self.tempLocations = self._parent.data
        if self.__prefix:
            self.tempLocations = [LocateItem(x, self.tempLocations[x])
                for x in self.tempLocations
                if x.lower().find(self.__prefix) > -1]
        else:
            self.tempLocations = [LocateItem(x, self.tempLocations[x])
                for x in self.tempLocations]
        return self.tempLocations

    def _refresh_filter(self):
        self.frame.refresh(self.filter())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            currentText = unicode(self.frame.listWidget.currentItem().text())
            self.setText(currentText)
            return

        QLineEdit.keyPressEvent(self, event)
        if event.key() == Qt.Key_Down:
            if self.frame.listWidget.currentRow() != \
              self.frame.listWidget.count() - 1:
                self.frame.listWidget.setCurrentRow(
                    self.frame.listWidget.currentRow() + 1)
        elif event.key() == Qt.Key_Up:
            if self.frame.listWidget.currentRow() > 0:
                self.frame.listWidget.setCurrentRow(
                    self.frame.listWidget.currentRow() - 1)
        elif event.key() in (Qt.Key_Tab, Qt.Key_Return, Qt.Key_Enter):
            item = self.frame.listWidget.currentItem()
            self.emit(SIGNAL("itemFound(QString)"), item.path)
            self.setText('')
            self.frame.hide()
            self._parent._parentTree.setFocus()
        elif event.key() == Qt.Key_Escape:
            self.frame.hide()
            self._parent._parentTree.setFocus()

    def focusOutEvent(self, event):
        if self.frame:
            self.frame.hide()
        QLineEdit.focusOutEvent(self, event)

    def focusInEvent(self, event):
        QLineEdit.focusOutEvent(self, event)
        self.complete()


class PopupCompleter(QFrame):

    def __init__(self, model):
        QFrame.__init__(self, None, Qt.FramelessWindowHint | Qt.ToolTip)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.listWidget = QListWidget()
        for i, item in enumerate(model):
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(0)
        vbox.addWidget(self.listWidget)

    def refresh(self, model):
        self.listWidget.clear()
        for i, item in enumerate(model):
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(0)
