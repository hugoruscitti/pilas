# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pilas/data/manual.ui'
#
# Created: Thu Feb 13 11:07:12 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ManualWindow(object):
    def setupUi(self, ManualWindow):
        ManualWindow.setObjectName(_fromUtf8("ManualWindow"))
        ManualWindow.resize(844, 508)
        ManualWindow.setMinimumSize(QtCore.QSize(500, 400))
        self.centralwidget = QtGui.QWidget(ManualWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.webView.setStatusTip(_fromUtf8(""))
        self.webView.setAccessibleDescription(_fromUtf8(""))
        self.webView.setProperty("url", QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        ManualWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ManualWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        ManualWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ManualWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ManualWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ManualWindow)
        QtCore.QMetaObject.connectSlotsByName(ManualWindow)

    def retranslateUi(self, ManualWindow):
        ManualWindow.setWindowTitle(_translate("ManualWindow", "manual de pilas-engine", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ManualWindow = QtGui.QMainWindow()
    ui = Ui_ManualWindow()
    ui.setupUi(ManualWindow)
    ManualWindow.show()
    sys.exit(app.exec_())

