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

from PyQt4 import QtCore
from PyQt4 import QtGui

from pilasengine.configuracion.configuracion_base import Ui_Dialog

AUDIO_HABILITADO = True
PAD_HABILITADO = False


class Dialogoconfiguracion(Ui_Dialog):

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Ui_Dialog.setupUi(self, Dialog)
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.fuente.connect(self.fuente,
                            QtCore.SIGNAL("clicked()"),
                            self.cuando_pulsa_el_boton_fuente)

    def cuando_pulsa_el_boton_fuente(self):
        font, ok = QtGui.QFontDialog.getFont()

        if ok:
            self.ejemplo.setFont(font)



def abrir(parent=None):
    print parent
    MainDialog = QtGui.QDialog(parent)

    d = Dialogoconfiguracion()
    d.setupUi(MainDialog)
    MainDialog.exec_()
    #MainDialog.raise_()

    return d
