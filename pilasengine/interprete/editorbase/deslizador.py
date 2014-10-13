# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from PyQt4 import QtGui
from PyQt4 import QtCore


class Deslizador(QtGui.QWidget):

    def __init__(self, parent, cursor, valor_inicial, funcion_cuando_cambia):
        QtGui.QWidget.__init__(self, parent)
        self.funcion_cuando_cambia = funcion_cuando_cambia

        layout = QtGui.QGridLayout(self)
        
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        layout.addWidget(self.slider)
        
        self.checkbox_es_float = QtGui.QCheckBox()
        self.checkbox_es_float.setText(u"Es número fraccionario")
        layout.addWidget(self.checkbox_es_float)
        
        self.checkbox_es_float.stateChanged.connect(self.cuando_pulsa_checkbox)
        
        self.slider.setMinimumWidth(200)
        
        self._definir_valor_inicial(valor_inicial)
        
        self.slider.valueChanged[int].connect(self.on_change)


        #layout.addWidget(slider)
        layout.setContentsMargins(7, 7, 7, 7)

        self.setLayout(layout)
        self.adjustSize()

        self.setWindowFlags(QtCore.Qt.Popup)

        point = parent.cursorRect(cursor).bottomRight()
        global_point = parent.mapToGlobal(point)

        self.move(global_point)
    
    def _definir_valor_inicial(self, valor_inicial):
        if '.' in str(valor_inicial):
            valor_inicial = int(float(valor_inicial) * 100)
            self.checkbox_es_float.setChecked(True)
        else:
            valor_inicial = int(str(valor_inicial))
            self.checkbox_es_float.setChecked(False)

        self.slider.setMaximum(valor_inicial + 300)
        self.slider.setMinimum(valor_inicial - 300)
        self.slider.setValue(valor_inicial)
    
    def cuando_pulsa_checkbox(self, state):
        if state:
            valor = float(self.slider.value()) + 0.0
        else:
            valor = int(self.slider.value()/100.0)
            
        self._definir_valor_inicial(valor)


    def on_change(self, valor):
        if self.checkbox_es_float.isChecked():
            valor = str(valor/100.0)
            self.funcion_cuando_cambia(str(valor))
        else:
            self.funcion_cuando_cambia(str(valor))