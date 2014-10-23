import sys
import signal

import importlib
from PyQt4 import *
from PyQt4 import Qt
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from PyQt4 import QtOpenGL
import Box2D
import pygame

import json
import new
import uuid
import code


pilasengine = __import__('pilasengine')


app = QtGui.QApplication(sys.argv)

pilasengine.configuracion.Configuracion()

if '-i' in sys.argv:
    from pilasengine import interprete
    _ = interprete.abrir()
elif '-t' in sys.argv:
    from pilasengine import utils
    utils.realizar_pruebas()
    sys.exit(1)
else:
    _ = pilasengine.abrir_asistente()

icono = pilasengine.utils.obtener_ruta_al_recurso('icono.ico')
app.setWindowIcon(QtGui.QIcon(icono))
#mainwindow.setWindowIcon(QtGui.QIcon(icono))

sys.exit(app.exec_())
