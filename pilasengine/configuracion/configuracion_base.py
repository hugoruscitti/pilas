# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pilasengine/configuracion/configuracion.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(500, 300)
        Dialog.setMinimumSize(QtCore.QSize(500, 300))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.fuente = QtGui.QPushButton(Dialog)
        self.fuente.setObjectName(_fromUtf8("fuente"))
        self.horizontalLayout_2.addWidget(self.fuente)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.gridLayout.addLayout(self.horizontalLayout_4, 7, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 76, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.guardar = QtGui.QPushButton(Dialog)
        self.guardar.setObjectName(_fromUtf8("guardar"))
        self.horizontalLayout.addWidget(self.guardar)
        self.gridLayout.addLayout(self.horizontalLayout, 9, 0, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(Dialog)
        self.checkBox_2.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout.addWidget(self.checkBox_2, 2, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.checkbox_aceleracion = QtGui.QCheckBox(Dialog)
        self.checkbox_aceleracion.setChecked(True)
        self.checkbox_aceleracion.setObjectName(_fromUtf8("checkbox_aceleracion"))
        self.gridLayout.addWidget(self.checkbox_aceleracion, 3, 0, 1, 1)
        self.checkbox_autocompletar = QtGui.QCheckBox(Dialog)
        self.checkbox_autocompletar.setObjectName(_fromUtf8("checkbox_autocompletar"))
        self.gridLayout.addWidget(self.checkbox_autocompletar, 4, 0, 1, 1)
        self.mensaje = QtGui.QLabel(Dialog)
        self.mensaje.setStyleSheet(_fromUtf8("color: red"))
        self.mensaje.setText(_fromUtf8("Estos cambios requiren que reinicies el intérprete."))
        self.mensaje.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mensaje.setObjectName(_fromUtf8("mensaje"))
        self.gridLayout.addWidget(self.mensaje, 6, 0, 1, 1)
        self.checkbox_atajos = QtGui.QCheckBox(Dialog)
        self.checkbox_atajos.setObjectName(_fromUtf8("checkbox_atajos"))
        self.gridLayout.addWidget(self.checkbox_atajos, 5, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Configuración", None))
        self.label.setText(_translate("Dialog", "Tipografía", None))
        self.fuente.setText(_translate("Dialog", "Cambiar", None))
        self.guardar.setText(_translate("Dialog", "Guardar", None))
        self.checkBox_2.setText(_translate("Dialog", "Soporte para joysticks.", None))
        self.checkBox.setText(_translate("Dialog", "Habilitar Audio.", None))
        self.checkbox_aceleracion.setText(_translate("Dialog", "Usar aceleración de video por hardware (OpenGL).", None))
        self.checkbox_autocompletar.setText(_translate("Dialog", "Sugerir código usando un menú contextual mientras escribe.", None))
        self.checkbox_atajos.setText(_translate("Dialog", "Activar atajos de teclado para cambiar fuentes (alt + y alt -)", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

