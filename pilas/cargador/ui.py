# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Tue May  3 16:55:22 2011
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
        MainWindow.resize(510, 520)
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imagen.sizePolicy().hasHeightForWidth())
        self.imagen.setSizePolicy(sizePolicy)
        self.imagen.setMinimumSize(QtCore.QSize(400, 300))
        self.imagen.setObjectName(_fromUtf8("imagen"))
        self.verticalLayout.addWidget(self.imagen)
        self.progreso = QtGui.QFrame(self.centralwidget)
        self.progreso.setMinimumSize(QtCore.QSize(0, 22))
        self.progreso.setFrameShape(QtGui.QFrame.NoFrame)
        self.progreso.setFrameShadow(QtGui.QFrame.Plain)
        self.progreso.setLineWidth(0)
        self.progreso.setObjectName(_fromUtf8("progreso"))
        self.progressBar = QtGui.QProgressBar(self.progreso)
        self.progressBar.setGeometry(QtCore.QRect(0, 0, 221, 21))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty(_fromUtf8("value"), -1)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.BottomToTop)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label = QtGui.QLabel(self.progreso)
        self.label.setGeometry(QtCore.QRect(50, 0, 131, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.progreso)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ejecutar = QtGui.QPushButton(self.centralwidget)
        self.ejecutar.setObjectName(_fromUtf8("ejecutar"))
        self.horizontalLayout.addWidget(self.ejecutar)
        self.fuente = QtGui.QPushButton(self.centralwidget)
        self.fuente.setObjectName(_fromUtf8("fuente"))
        self.horizontalLayout.addWidget(self.fuente)
        self.guardar = QtGui.QPushButton(self.centralwidget)
        self.guardar.setObjectName(_fromUtf8("guardar"))
        self.horizontalLayout.addWidget(self.guardar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.codigo = QtGui.QTextEdit(self.centralwidget)
        self.codigo.setReadOnly(True)
        self.codigo.setObjectName(_fromUtf8("codigo"))
        self.verticalLayout.addWidget(self.codigo)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 510, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArchivo = QtGui.QMenu(self.menubar)
        self.menuArchivo.setObjectName(_fromUtf8("menuArchivo"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSalir = QtGui.QAction(MainWindow)
        self.actionSalir.setObjectName(_fromUtf8("actionSalir"))
        self.menuArchivo.addAction(self.actionSalir)
        self.menubar.addAction(self.menuArchivo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Ejemplos del motor pilas", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Cargando ejemplo", None, QtGui.QApplication.UnicodeUTF8))
        self.ejecutar.setText(QtGui.QApplication.translate("MainWindow", "Ejecutar", None, QtGui.QApplication.UnicodeUTF8))
        self.fuente.setText(QtGui.QApplication.translate("MainWindow", "Cambiar tipografia", None, QtGui.QApplication.UnicodeUTF8))
        self.guardar.setText(QtGui.QApplication.translate("MainWindow", "Guardar Codigo", None, QtGui.QApplication.UnicodeUTF8))
        self.menuArchivo.setTitle(QtGui.QApplication.translate("MainWindow", "Archivo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSalir.setText(QtGui.QApplication.translate("MainWindow", "Salir", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

