# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pilas/data/manual.ui'
#
# Created: Fri Sep 27 16:36:32 2013
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_ManualDialog(object):
    def setupUi(self, ManualDialog):
        ManualDialog.setObjectName(_fromUtf8("ManualDialog"))
        ManualDialog.resize(783, 507)
        self.horizontalLayout = QtGui.QHBoxLayout(ManualDialog)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.webView = QtWebKit.QWebView(ManualDialog)
        self.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.webView.setStatusTip(_fromUtf8(""))
        self.webView.setAccessibleDescription(_fromUtf8(""))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.horizontalLayout.addWidget(self.webView)

        self.retranslateUi(ManualDialog)
        QtCore.QMetaObject.connectSlotsByName(ManualDialog)

    def retranslateUi(self, ManualDialog):
        ManualDialog.setWindowTitle(_translate("ManualDialog", "Manual de pilas-engine", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ManualDialog = QtGui.QDialog()
    ui = Ui_ManualDialog()
    ui.setupUi(ManualDialog)
    ManualDialog.show()
    sys.exit(app.exec_())

