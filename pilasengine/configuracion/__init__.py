# -*- coding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
import sys
import re
import codecs
import time
import pickle

from PyQt4 import QtCore
from PyQt4 import QtGui

from pilasengine.configuracion.configuracion_base import Ui_Dialog

AUDIO_HABILITADO = True
PAD_HABILITADO = False

class Configuracion(object):

    def __init__(self):
        self.valores = {}
        self.cargar()

    def cargar(self):
        if os.path.exists(self.obtener_ruta()):
            archivo = open(self.obtener_ruta(), 'rb')
            self.valores = pickle.load(archivo)
            archivo.close()
        else:
            self.valores = self.obtener_datos_por_omision()
            self.guardar()

    def obtener_datos_por_omision(self):
        datos = {
                'fuente': 'Monaco 20',
                'audio_habilitado': False,
                'pad_habilitado': False,
                }
        return datos

    def guardar(self):
        archivo = open(self.obtener_ruta(), 'wb')
        pickle.dump(self.valores, archivo)
        archivo.close()

    def obtener_ruta(self):
        return "configuracion.cfg"

    def cambiar_fuente(self, fuente_nueva):
        self.valores['fuente'] = fuente_nueva

    def obtener_fuente(self):
        fuente_como_tupla = self.valores['fuente'].rsplit(' ', 1)
        return QtGui.QFont(fuente_como_tupla[0], int(fuente_como_tupla[1]))


class DialogoConfiguracion(Ui_Dialog):

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Ui_Dialog.setupUi(self, Dialog)
        self._conectar_eventos()
        self.configuracion = Configuracion()
        self.definir_fuente(self.configuracion.obtener_fuente())

    def _conectar_eventos(self):
        self.fuente.connect(self.fuente,
                            QtCore.SIGNAL("clicked()"),
                            self.cuando_pulsa_el_boton_fuente)
        self.guardar.connect(self.guardar,
                            QtCore.SIGNAL("clicked()"),
                            self.cuando_pulsa_el_boton_guardar)

    def cuando_pulsa_el_boton_fuente(self):
        font, ok = QtGui.QFontDialog.getFont()

        if ok:
            etiqueta = "%s %d" %(font.rawName(), font.pointSize())
            self.configuracion.cambiar_fuente(etiqueta)
            self.configuracion.guardar()
            self.definir_fuente(self.configuracion.obtener_fuente())

    def definir_fuente(self, font):
        etiqueta = "%s %d" %(font.rawName(), font.pointSize())
        self.ejemplo.setText(etiqueta)
        self.ejemplo.setFont(font)

    def cuando_pulsa_el_boton_guardar(self):
        self.Dialog.close()

def abrir(parent=None):
    MainDialog = QtGui.QDialog(parent)

    d = DialogoConfiguracion()
    d.setupUi(MainDialog)
    MainDialog.exec_()
    #MainDialog.raise_()

    return d