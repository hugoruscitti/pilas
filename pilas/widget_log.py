# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import os
from PyQt4 import QtGui, QtCore

class WidgetLog(QtGui.QMainWindow):
    """ Representa una ventana de log.
    Mediante pilas.log.imprimir() añadiremos elementos a esta ventana
    """
    def __init__(self):
        super(WidgetLog, self).__init__()
        self._initUI()

        self._ejecutando = True

    def _initUI(self):

        self.setWindowTitle('Pilas Log')

        self.setWindowIcon(QtGui.QIcon(self._ruta_icono('tux.png')))

        self.centralwidget = QtGui.QWidget(self)

        accionSalir = QtGui.QAction(QtGui.QIcon(self._ruta_icono('door_out.png')), 'Salir', self)
        accionSalir.setShortcut('Ctrl+S')
        accionSalir.triggered.connect(self.close)

        accionEjecutar = QtGui.QAction(QtGui.QIcon(self._ruta_icono('control_play.png')), 'Ejecutar', self)
        accionEjecutar.setShortcut('Ctrl+E')
        accionEjecutar.triggered.connect(self._ejecutar)

        accionPausar = QtGui.QAction(QtGui.QIcon(self._ruta_icono('control_pause.png')), 'Pausar', self)
        accionPausar.setShortcut('Ctrl+P')
        accionPausar.triggered.connect(self._pausar)

        accionResetear = QtGui.QAction(QtGui.QIcon(self._ruta_icono('arrow_refresh.png')), 'Resetear', self)
        accionResetear.setShortcut('Ctrl+R')
        accionResetear.triggered.connect(self._resetear)

        self.toolbar = self.addToolBar('Acciones')
        self.toolbar.addAction(accionSalir)
        self.toolbar.addAction(accionEjecutar)
        self.toolbar.addAction(accionPausar)
        self.toolbar.addAction(accionResetear)

        hbox = QtGui.QHBoxLayout(self.centralwidget)

        self.treeView = QtGui.QTreeWidget(self.centralwidget)

        self.treeView.setColumnCount(2)

        cabecera = QtCore.QStringList()
        cabecera.append("Clave")
        cabecera.append("Valor")

        self.treeView.setHeaderLabels(cabecera)

        hbox.addWidget(self.treeView)

        self.setCentralWidget(self.centralwidget)

        self._ejecutar()

        self.setGeometry(50, 50, 250, 250)
        self.show()

    def _ejecutar(self):
        self._ejecutando = True
        self.statusBar().showMessage('Ejecutando')

    def _pausar(self):
        self._ejecutando = False
        self.statusBar().showMessage('Pausado')

    def _resetear(self):
        self.treeView.clear()
        self._ejecutar()

    def _ruta_icono(self, icono):
        return os.path.join('data' , 'iconos', icono)

    def imprimir(self, params):
        if (self._ejecutando):
            for elemento in params:
                self._insertar_elemento(elemento)

            self.treeView.header().setResizeMode(3)

    def _insertar_elemento(self, elemento, elemento_padre=None):

        if (self._contiene_diccionario(elemento)):
            if (hasattr(elemento, '__class__')):
                if (elemento.__class__.__name__ != 'dict'):
                    padre = self._insertar_texto_en_lista(elemento.__class__.__name__, elemento_padre)
                else:
                    padre = None
            else:
                padre = None

            for key, value in self._obtener_diccionario(elemento):
                if (key != "escena"):
                    if self._contiene_diccionario(value):
                        self._insertar_elemento(value, self._insertar_texto_en_lista(key, padre))
                    else:
                        self._insertar_diccionario_en_lista(key, value, padre)
        else:
            self._insertar_texto_en_lista(str(elemento))

    def _contiene_diccionario(self, valor):
        if hasattr(valor, '__dict__'):
            return True
        elif type(valor) is dict:
            return True
        else:
            return False

    def _obtener_diccionario(self, valor):
        if hasattr(valor, '__dict__'):
            return valor.__dict__.items()
        elif type(valor) is dict:
            return valor.items()

    def _insertar_texto_en_lista(self, texto, itemPadre=None):
        if (itemPadre == None):
            item = QtGui.QTreeWidgetItem(self.treeView)
        else:
            item = QtGui.QTreeWidgetItem(itemPadre)
        item.setText(0, str(texto))
        return item

    def _insertar_diccionario_en_lista(self, clave, valor, itemPadre=None):
        if (itemPadre == None):
            item = QtGui.QTreeWidgetItem(self.treeView)
        else:
            item = QtGui.QTreeWidgetItem(itemPadre)
        item.setText(0, str(clave))
        item.setText(1, str(valor))
        return item




