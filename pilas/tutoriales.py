# -*- coding: utf-8 -*-
import os
import sys

try:
    from PyQt4 import QtCore, QtGui
    from .tutoriales_base import Ui_TutorialesWindow
except:
    print("ERROR: No se encuentra pyqt")
    Ui_TutorialesWindow = object
    pass

import os
import pilas

class VentanaTutoriales(Ui_TutorialesWindow):

    def setupUi(self, main):
        self.main = main
        Ui_TutorialesWindow.setupUi(self, main)
        pilas.utils.centrar_ventana(main)
        self.cargar_tutoriales()

    def cargar_tutoriales(self):
        file_path = pilas.utils.obtener_ruta_al_recurso('tutoriales/index.html')
        file_path = os.path.abspath(file_path)

        base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        self.webView.load(base_dir)
        self.webView.history().setMaximumItemCount(0)

def main(parent=None, do_raise=False):
    dialog = QtGui.QMainWindow(parent)
    dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)
    ui = VentanaTutoriales()
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
