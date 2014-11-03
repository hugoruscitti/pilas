# -*- coding: utf-8 -*-
import os
import sys

try:
    from PyQt4 import QtCore, QtGui
    from .manual_base import Ui_ManualWindow
except:
    print("ERROR: No se encuentra pyqt")
    Ui_ManualWindow = object
    pass

import os
import pilas

class VentanaManual(Ui_ManualWindow):

    def setupUi(self, main):
        self.main = main
        Ui_ManualWindow.setupUi(self, main)
        pilas.utils.centrar_ventana(main)
        self.cargar_manual()

    def cargar_manual(self):
        file_path = pilas.utils.obtener_ruta_al_recurso('manual/index.html')
        file_path = os.path.abspath(file_path)

        base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        self.webView.load(base_dir)
        self.webView.history().setMaximumItemCount(0)

def main(parent=None, do_raise=False):
    dialog = QtGui.QMainWindow(parent)
    dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)
    ui = VentanaManual()
    ui.setupUi(dialog)
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    #if sys.platform == 'darwin':
    #    if getattr(sys, 'frozen', None):
    #        dialog.showMinimized()
    #        dialog.showNormal()
						
    dialog.show()

    if do_raise:
        dialog.raise_()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("pilas-engine")
    main()
