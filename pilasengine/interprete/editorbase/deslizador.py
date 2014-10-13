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
    """Representa el popup que nos permite ajustar valores numéricos.
    
    Este popup aparece cuando se pulsa el botón derecho del mouse
    sobre una sentencia que tenga una asignación de valor en un atributo,
    por ejemplo algo como: ``actor.escala = 1``.
    """
    
    def __init__(self, parent, cursor, valor_inicial, funcion_cuando_cambia):
        QtGui.QWidget.__init__(self, parent)
        self.funcion_cuando_cambia = funcion_cuando_cambia

        self._crear_interfaz()        
        self._definir_valor_inicial(valor_inicial)

        self._posicionar_ventana_debajo_del_mouse(parent, cursor)

    def _crear_interfaz(self):
        self.layout = QtGui.QGridLayout(self)
        
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimumWidth(200)
        self.slider.valueChanged[int].connect(self.on_change)
        
        self.checkbox_es_float = QtGui.QCheckBox()
        self.checkbox_es_float.setText(u"Es número fraccionario")
        self.checkbox_es_float.stateChanged.connect(self.cuando_pulsa_checkbox)
        
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.checkbox_es_float)
        self.layout.setContentsMargins(7, 7, 7, 7)
        
        self.setLayout(self.layout)
        self.adjustSize()
        self.setWindowFlags(QtCore.Qt.Popup)
        
    def _posicionar_ventana_debajo_del_mouse(self, parent, cursor):
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