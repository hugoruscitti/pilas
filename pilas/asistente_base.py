# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asistente.ui'
#
# Created: Sat Oct  6 20:19:10 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AsistenteWindow(object):
    def setupUi(self, AsistenteWindow):
        AsistenteWindow.setObjectName(_fromUtf8("AsistenteWindow"))
        AsistenteWindow.resize(507, 342)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pilas.ico")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        AsistenteWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(AsistenteWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        AsistenteWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AsistenteWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 507, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        AsistenteWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AsistenteWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AsistenteWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AsistenteWindow)
        QtCore.QMetaObject.connectSlotsByName(AsistenteWindow)

    def retranslateUi(self, AsistenteWindow):
        AsistenteWindow.setWindowTitle(QtGui.QApplication.translate("AsistenteWindow", "pilas-engine", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    AsistenteWindow = QtGui.QMainWindow()
    ui = Ui_AsistenteWindow()
    ui.setupUi(AsistenteWindow)
    AsistenteWindow.show()
    sys.exit(app.exec_())

