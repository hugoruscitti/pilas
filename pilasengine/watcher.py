# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
from PyQt4 import QtGui
from PyQt4 import QtCore

class Watcher(QtCore.QObject):

    def __init__(self, aFile, callback=None, checkEvery=2):
        super(Watcher, self).__init__()

        self.file = aFile
        self.callback = callback
        self.ultima_modificacion = os.path.getmtime(self.file)

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery*1000)
        self._timer.timeout.connect(self._checkFile)
        self._timer.start()

    def _checkFile(self):
        modificacion = os.path.getmtime(self.file)

        if modificacion != self.ultima_modificacion:
            if self.callback:
                self.callback()

            self.ultima_modificacion = modificacion