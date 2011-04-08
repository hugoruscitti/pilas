# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Fri Apr  8 00:49:07 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(513, 350)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lista = QtGui.QListWidget(self.centralwidget)
        self.lista.setObjectName(_fromUtf8("lista"))
        self.gridLayout.addWidget(self.lista, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.imagen = QtGui.QGraphicsView(self.centralwidget)
        self.imagen.setObjectName(_fromUtf8("imagen"))
        self.verticalLayout.addWidget(self.imagen)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ejecutar = QtGui.QPushButton(self.centralwidget)
        self.ejecutar.setObjectName(_fromUtf8("ejecutar"))
        self.horizontalLayout.addWidget(self.ejecutar)
        self.guardar = QtGui.QPushButton(self.centralwidget)
        self.guardar.setObjectName(_fromUtf8("guardar"))
        self.horizontalLayout.addWidget(self.guardar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.codigo = QtGui.QTextEdit(self.centralwidget)
        self.codigo.setObjectName(_fromUtf8("codigo"))
        self.verticalLayout.addWidget(self.codigo)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 513, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Ejemplos del motor pilas", None, QtGui.QApplication.UnicodeUTF8))
        self.ejecutar.setText(QtGui.QApplication.translate("MainWindow", "Ejecutar", None, QtGui.QApplication.UnicodeUTF8))
        self.guardar.setText(QtGui.QApplication.translate("MainWindow", "Guardar Codigo", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

