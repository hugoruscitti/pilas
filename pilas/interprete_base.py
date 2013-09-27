# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pilas/data/interprete.ui'
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

class Ui_InterpreteDialog(object):
    def setupUi(self, InterpreteDialog):
        InterpreteDialog.setObjectName(_fromUtf8("InterpreteDialog"))
        InterpreteDialog.resize(770, 681)
        self.gridLayout = QtGui.QGridLayout(InterpreteDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter_vertical = QtGui.QSplitter(InterpreteDialog)
        self.splitter_vertical.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_vertical.setObjectName(_fromUtf8("splitter_vertical"))
        self.navegador = QtWebKit.QWebView(self.splitter_vertical)
        self.navegador.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.navegador.setObjectName(_fromUtf8("navegador"))
        self.splitter = QtGui.QSplitter(self.splitter_vertical)
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
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.manual_button = QtGui.QPushButton(self.layoutWidget)
        self.manual_button.setCheckable(True)
        self.manual_button.setFlat(True)
        self.manual_button.setObjectName(_fromUtf8("manual_button"))
        self.horizontalLayout_2.addWidget(self.manual_button)
        spacerItem = QtGui.QSpacerItem(37, 13, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_6 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_6.setMaximumSize(QtCore.QSize(26, 26))
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setCheckable(True)
        self.pushButton_6.setFlat(True)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.pushButton_5 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_5.setMaximumSize(QtCore.QSize(26, 26))
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setCheckable(True)
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_4 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_4.setMaximumSize(QtCore.QSize(26, 26))
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setCheckable(True)
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_3 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_3.setMaximumSize(QtCore.QSize(26, 26))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_2 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_2.setMaximumSize(QtCore.QSize(26, 26))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(26, 26))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setToolTip(_fromUtf8(""))
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.console = QtGui.QStackedWidget(self.layoutWidget)
        self.console.setObjectName(_fromUtf8("console"))
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.console.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.console.addWidget(self.page_4)
        self.verticalLayout.addWidget(self.console)
        self.gridLayout.addWidget(self.splitter_vertical, 0, 0, 1, 1)

        self.retranslateUi(InterpreteDialog)
        self.console.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(InterpreteDialog)

    def retranslateUi(self, InterpreteDialog):
        InterpreteDialog.setWindowTitle(_translate("InterpreteDialog", "pilas-engine interprete", None))
        self.manual_button.setText(_translate("InterpreteDialog", "Manual", None))
        self.pushButton_6.setText(_translate("InterpreteDialog", "F7", None))
        self.pushButton_5.setText(_translate("InterpreteDialog", "F8", None))
        self.pushButton_4.setText(_translate("InterpreteDialog", "F9", None))
        self.pushButton_3.setText(_translate("InterpreteDialog", "F10", None))
        self.pushButton_2.setText(_translate("InterpreteDialog", "F11", None))
        self.pushButton.setText(_translate("InterpreteDialog", "F12", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    InterpreteDialog = QtGui.QDialog()
    ui = Ui_InterpreteDialog()
    ui.setupUi(InterpreteDialog)
    InterpreteDialog.show()
    sys.exit(app.exec_())

