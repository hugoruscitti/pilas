# -*- encoding: utf-8 -*-
import tkMessageBox
import Tkinter
import imp
import sys
import os

window = Tkinter.Tk()
window.wm_withdraw()


if not os.path.exists('ejecutar.py'):
    tkMessageBox.showerror("Cargador de pilas-engine", "No se encuentra el archivo ejecutar.py")
    sys.exit(1)

try:
    imp.load_source("__main__", "ejecutar.py")
except Exception, e:
    tkMessageBox.showerror("Error al ejecutar ejecutar.py", e)
    sys.exit(1)
