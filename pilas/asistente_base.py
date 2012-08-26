# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asistente.ui'
#
# Created: Sun Aug 26 19:14:54 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName(_fromUtf8("Main"))
        Main.resize(457, 321)
        self.gridLayout = QtGui.QGridLayout(Main)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webView = QtWebKit.QWebView(Main)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        Main.setWindowTitle(QtGui.QApplication.translate("Main", "pilas engine", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Main = QtGui.QDialog()
    ui = Ui_Main()
    ui.setupUi(Main)
    Main.show()
    sys.exit(app.exec_())

