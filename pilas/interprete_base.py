# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interprete.ui'
#
# Created: Tue Aug 28 17:43:39 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InterpreteDialog(object):
    def setupUi(self, InterpreteDialog):
        InterpreteDialog.setObjectName(_fromUtf8("InterpreteDialog"))
        InterpreteDialog.resize(642, 554)
        self.gridLayout = QtGui.QGridLayout(InterpreteDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(InterpreteDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.canvas = QtGui.QStackedWidget(self.splitter)
        self.canvas.setMinimumSize(QtCore.QSize(320, 240))
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

        self.retranslateUi(InterpreteDialog)
        QtCore.QMetaObject.connectSlotsByName(InterpreteDialog)

    def retranslateUi(self, InterpreteDialog):
        InterpreteDialog.setWindowTitle(QtGui.QApplication.translate("InterpreteDialog", "pilas-engine interprete", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    InterpreteDialog = QtGui.QDialog()
    ui = Ui_InterpreteDialog()
    ui.setupUi(InterpreteDialog)
    InterpreteDialog.show()
    sys.exit(app.exec_())

