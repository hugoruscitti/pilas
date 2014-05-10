# -*- encoding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore


class Deslizador(QtGui.QWidget):

    def __init__(self, parent, cursor, valor_inicial, funcion_cuando_cambia):
        QtGui.QWidget.__init__(self, parent)
        self.funcion_cuando_cambia = funcion_cuando_cambia

        layout = QtGui.QGridLayout(self)
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)

        slider.setMinimumWidth(200)

        if '.' in str(valor_inicial):
            valor_inicial = int(float(valor_inicial) * 100)
            slider.valueChanged[int].connect(self.on_change_float)
        else:
            valor_inicial = int(str(valor_inicial))
            slider.valueChanged[int].connect(self.on_change)

        slider.setMaximum(valor_inicial + 300)
        slider.setMinimum(valor_inicial - 300)
        slider.setValue(valor_inicial)

        layout.addWidget(slider)
        layout.setContentsMargins(7, 7, 7, 7)

        self.setLayout(layout)
        self.adjustSize()

        self.setWindowFlags(QtCore.Qt.Popup)

        point = parent.cursorRect(cursor).bottomRight()
        global_point = parent.mapToGlobal(point)

        self.move(global_point)

    def on_change(self, valor):
        self.funcion_cuando_cambia(str(valor))

    def on_change_float(self, valor):
        valor = str(valor/100.0)
        self.funcion_cuando_cambia(str(valor))