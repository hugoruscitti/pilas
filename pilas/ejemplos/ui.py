# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Fri Aug 22 14:23:59 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Ejemplos(object):
    def setupUi(self, Ejemplos):
        Ejemplos.setObjectName(_fromUtf8("Ejemplos"))
        Ejemplos.resize(787, 493)
        self.gridLayout = QtGui.QGridLayout(Ejemplos)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter_2 = QtGui.QSplitter(Ejemplos)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.vbox_left = QtGui.QWidget(self.splitter_2)
        self.vbox_left.setObjectName(_fromUtf8("vbox_left"))
        self.vlayout_left = QtGui.QVBoxLayout(self.vbox_left)
        self.vlayout_left.setMargin(0)
        self.vlayout_left.setObjectName(_fromUtf8("vlayout_left"))
        self.arbol = QtGui.QTreeWidget(self.vbox_left)
        self.arbol.setObjectName(_fromUtf8("arbol"))
        self.arbol.headerItem().setText(0, _fromUtf8("1"))
        self.vlayout_left.addWidget(self.arbol)
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.imagen = QtGui.QGraphicsView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imagen.sizePolicy().hasHeightForWidth())
        self.imagen.setSizePolicy(sizePolicy)
        self.imagen.setMinimumSize(QtCore.QSize(400, 300))
        self.imagen.setAutoFillBackground(True)
        self.imagen.setRenderHints(QtGui.QPainter.SmoothPixmapTransform)
        self.imagen.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.imagen.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.imagen.setViewportUpdateMode(QtGui.QGraphicsView.SmartViewportUpdate)
        self.imagen.setObjectName(_fromUtf8("imagen"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progreso = QtGui.QFrame(self.layoutWidget)
        self.progreso.setMinimumSize(QtCore.QSize(0, 22))
        self.progreso.setFrameShape(QtGui.QFrame.NoFrame)
        self.progreso.setFrameShadow(QtGui.QFrame.Plain)
        self.progreso.setLineWidth(0)
        self.progreso.setObjectName(_fromUtf8("progreso"))
        self.label = QtGui.QLabel(self.progreso)
        self.label.setGeometry(QtCore.QRect(6, 0, 170, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.progreso)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ejecutar = QtGui.QPushButton(self.layoutWidget)
        self.ejecutar.setObjectName(_fromUtf8("ejecutar"))
        self.horizontalLayout.addWidget(self.ejecutar)
        self.fuente = QtGui.QPushButton(self.layoutWidget)
        self.fuente.setObjectName(_fromUtf8("fuente"))
        self.horizontalLayout.addWidget(self.fuente)
        self.guardar = QtGui.QPushButton(self.layoutWidget)
        self.guardar.setObjectName(_fromUtf8("guardar"))
        self.horizontalLayout.addWidget(self.guardar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.codigo = QtGui.QTextEdit(self.layoutWidget)
        self.codigo.setReadOnly(True)
        self.codigo.setObjectName(_fromUtf8("codigo"))
        self.verticalLayout.addWidget(self.codigo)
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.retranslateUi(Ejemplos)
        QtCore.QMetaObject.connectSlotsByName(Ejemplos)

    def retranslateUi(self, Ejemplos):
        Ejemplos.setWindowTitle(QtGui.QApplication.translate("Ejemplos", "Explorador de ejemplos", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Ejemplos", "Aguarde por favor ...", None, QtGui.QApplication.UnicodeUTF8))
        self.ejecutar.setText(QtGui.QApplication.translate("Ejemplos", "Ejecutar", None, QtGui.QApplication.UnicodeUTF8))
        self.fuente.setText(QtGui.QApplication.translate("Ejemplos", "Cambiar tipografia", None, QtGui.QApplication.UnicodeUTF8))
        self.guardar.setText(QtGui.QApplication.translate("Ejemplos", "Guardar Codigo", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Ejemplos = QtGui.QDialog()
    ui = Ui_Ejemplos()
    ui.setupUi(Ejemplos)
    Ejemplos.show()
    sys.exit(app.exec_())

