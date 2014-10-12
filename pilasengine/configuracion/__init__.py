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
import json

from PyQt4 import QtCore
from PyQt4 import QtGui

from pilasengine.configuracion.configuracion_base import Ui_Dialog

AUDIO_HABILITADO = False
PAD_HABILITADO = False

class Configuracion(object):

    def __init__(self):
        self.valores = {}
        self.cargar()

    def cargar(self):

        if os.path.exists(self.obtener_ruta()):
            with open(self.obtener_ruta(), 'rt') as archivo:
                self.valores = json.load(archivo, 'ascii')
        else:
            self.valores = self.obtener_datos_por_omision()
            self.guardar()

    def obtener_datos_por_omision(self):
        font_path = self._buscar_fuente_personalizada()

        if font_path:
            fuente_id = QtGui.QFontDatabase.addApplicationFont(font_path)
            fuente = str(QtGui.QFontDatabase.applicationFontFamilies(fuente_id)[0])
        else:
            fuente = "Courier New"

        datos = {
                'fuente': fuente + ' 15',
                'audio_habilitado': False,
                'pad_habilitado': False,
                'version': '1', # Versión del formato de configuración.
                }

        return datos

    def guardar(self):
        with open(self.obtener_ruta(), 'w') as archivo:
            json.dump(self.valores, archivo, sort_keys=True, indent=4, ensure_ascii=True)

    def obtener_ruta(self):
        ruta = os.path.join(str(QtCore.QDir.homePath()), '.configuracion_pilas.json')
        return ruta

    def cambiar_fuente(self, fuente_nueva):
        self.valores['fuente'] = fuente_nueva

    def obtener_fuente(self):
        fuente_como_tupla = self.valores['fuente'].rsplit(' ', 1)
        return QtGui.QFont(fuente_como_tupla[0], int(fuente_como_tupla[1]))

    def audio_habilitado(self):
        return self.valores['audio_habilitado']
    
    def pad_habilitado(self):
        return self.valores['pad_habilitado']

    def _buscar_fuente_personalizada(self):
        this_dir = os.path.dirname(os.path.realpath('.'))
        font_path = os.path.join(this_dir, 'SourceCodePro-Regular.ttf')

        if os.path.exists(font_path):
            return font_path

        font_path = os.path.join("./data/fuentes", 'SourceCodePro-Regular.ttf')

        if os.path.exists(font_path):
            return font_path

        this_dir = os.path.dirname(__file__)
        font_path = os.path.join(this_dir, 'SourceCodePro-Regular.ttf')

        if os.path.exists(font_path):
            return font_path

        return None

class DialogoConfiguracion(Ui_Dialog):

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Ui_Dialog.setupUi(self, Dialog)
        self._conectar_eventos()
        self.configuracion = Configuracion()
        self.definir_fuente(self.configuracion.obtener_fuente())
        
        self.checkBox.setChecked(self.configuracion.audio_habilitado())
        self.checkBox_2.setChecked(self.configuracion.pad_habilitado())    

    def _conectar_eventos(self):
        self.fuente.connect(self.fuente,
                            QtCore.SIGNAL("clicked()"),
                            self.cuando_pulsa_el_boton_fuente)
        self.guardar.connect(self.guardar,
                            QtCore.SIGNAL("clicked()"),
                            self.cuando_pulsa_el_boton_guardar)

    def cuando_pulsa_el_boton_fuente(self):
        font, ok = QtGui.QFontDialog.getFont(self.configuracion.obtener_fuente())

        if ok:
            etiqueta = "%s %d" %(font.rawName(), font.pointSize())
            self.configuracion.cambiar_fuente(etiqueta)
            self.configuracion.guardar()
            self.definir_fuente(self.configuracion.obtener_fuente())

    def definir_fuente(self, font):
        etiqueta = "%s %d" %(font.rawName(), font.pointSize())
        self.fuente.setText(etiqueta)

    def cuando_pulsa_el_boton_guardar(self):
        self.Dialog.close()

def abrir(parent=None):
    MainDialog = QtGui.QDialog(parent)

    d = DialogoConfiguracion()
    d.setupUi(MainDialog)
    MainDialog.exec_()
    #MainDialog.raise_()

    return d
