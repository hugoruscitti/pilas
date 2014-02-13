# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pilas/data/tutoriales.ui'
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

class Ui_TutorialesWindow(object):
    def setupUi(self, TutorialesWindow):
        TutorialesWindow.setObjectName(_fromUtf8("TutorialesWindow"))
        TutorialesWindow.resize(844, 508)
        TutorialesWindow.setMinimumSize(QtCore.QSize(500, 400))
        self.centralwidget = QtGui.QWidget(TutorialesWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.webView.setStatusTip(_fromUtf8(""))
        self.webView.setAccessibleDescription(_fromUtf8(""))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        TutorialesWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TutorialesWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        TutorialesWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TutorialesWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        TutorialesWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TutorialesWindow)
        QtCore.QMetaObject.connectSlotsByName(TutorialesWindow)

    def retranslateUi(self, TutorialesWindow):
        TutorialesWindow.setWindowTitle(_translate("TutorialesWindow", "Tutoriales de pilas-engine", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TutorialesWindow = QtGui.QMainWindow()
    ui = Ui_TutorialesWindow()
    ui.setupUi(TutorialesWindow)
    TutorialesWindow.show()
    sys.exit(app.exec_())

