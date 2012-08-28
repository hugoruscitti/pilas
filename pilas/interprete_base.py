# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interprete.ui'
#
# Created: Tue Aug 28 00:37:41 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InterpreteWindow(object):
    def setupUi(self, InterpreteWindow):
        InterpreteWindow.setObjectName(_fromUtf8("InterpreteWindow"))
        InterpreteWindow.resize(660, 615)
        self.centralwidget = QtGui.QWidget(InterpreteWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.canvas = QtGui.QStackedWidget(self.splitter)
        self.canvas.setMinimumSize(QtCore.QSize(200, 100))
        self.canvas.setObjectName(_fromUtf8("canvas"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.canvas.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.canvas.addWidget(self.page_2)
        self.console = QtGui.QStackedWidget(self.splitter)
        self.console.setObjectName(_fromUtf8("console"))
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.console.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.console.addWidget(self.page_4)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        InterpreteWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(InterpreteWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 660, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        InterpreteWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(InterpreteWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        InterpreteWindow.setStatusBar(self.statusbar)

        self.retranslateUi(InterpreteWindow)
        QtCore.QMetaObject.connectSlotsByName(InterpreteWindow)

    def retranslateUi(self, InterpreteWindow):
        InterpreteWindow.setWindowTitle(QtGui.QApplication.translate("InterpreteWindow", "pilas-engine", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    InterpreteWindow = QtGui.QMainWindow()
    ui = Ui_InterpreteWindow()
    ui.setupUi(InterpreteWindow)
    InterpreteWindow.show()
    sys.exit(app.exec_())

