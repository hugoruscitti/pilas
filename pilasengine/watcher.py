# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
import glob

from PyQt4 import QtGui
from PyQt4 import QtCore

class Watcher(QtCore.QObject):

    def __init__(self, aFile=None, callback=None, checkEvery=2):
        super(Watcher, self).__init__()

        self._cantidad_archivos_py = -1
        self._sumatoria_mtime = 0
        self.ultima_modificacion = 0
        self.cambiar_archivo_a_observar(aFile)
        self.callback = callback

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)
        self._timer.start()

    def cambiar_archivo_a_observar(self, aFile):
        if aFile:
            self.file = os.path.dirname(os.path.realpath(aFile))
            self._actualizar_contadores_de_archivos()
            self.ultima_modificacion = os.path.getmtime(self.file)
        else:
            self.file = None

    def _actualizar_contadores_de_archivos(self):
        self._sumatoria_mtime = 0
        archivos_py = glob.glob(self.file + "/*.py")

        for name in archivos_py:
            self._sumatoria_mtime += os.path.getmtime(name)

        self._cantidad_archivos_py = len(archivos_py)

    def prevenir_reinicio(self):
        if self.file:
            self._actualizar_contadores_de_archivos()
            #self.ultima_modificacion = os.path.getmtime(self.file)

    def _checkFile(self):
        if not self.file:
            return

        #modificacion = os.path.getmtime(self.file)

        # Valores anteriores
        anterior_cantidad_archivos_py = self._cantidad_archivos_py
        anterior_sumatoria_mtime = self._sumatoria_mtime

        self._actualizar_contadores_de_archivos()

        #if modificacion != self.ultima_modificacion: # Existe un cambio en el directorio

        if anterior_cantidad_archivos_py != self._cantidad_archivos_py or anterior_sumatoria_mtime != self._sumatoria_mtime:
            if self.callback:
                self.callback()

            #self.ultima_modificacion = modificacion
