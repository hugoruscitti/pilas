#!/usr/bin/python
# -*- encoding: utf-8
import sys
sys.path.append('..')

import pilas
pilas.utils.iniciar_asistente_desde_argumentos()

"""
#!/usr/bin/python
# -*- encoding: utf-8
#
# Este script permite crear una aplicación para Mac OS X con
# el siguiente comando:
#
#     python setup-mac.py py2app
#
# La aplicación se generará dentro del directorio dist.
import sys
import os
sys.path.append('..')

from optparse import OptionParser
import pilas

analizador = OptionParser()

analizador.add_option("-i", "--interprete", dest="interprete",
        action="store_true", default=False,
        help="Abre el interprete interactivo")

(opciones, argumentos) = analizador.parse_args()

if argumentos:
    archivo_a_ejecutar = pilas.utils.obtener_archivo_a_ejecutar_desde_argv()

    try:
        if archivo_a_ejecutar.startswith("-i"):
            archivo_a_ejecutar = archivo_a_ejecutar.replace("-i ", "")

        directorio_juego = os.path.dirname(archivo_a_ejecutar)
        os.chdir(directorio_juego)
        sys.exit(execfile(archivo_a_ejecutar))
    except Exception, e:
        pilas.utils.mostrar_mensaje_de_error_y_salir(str(e))

if opciones.interprete or '-i' in sys.argv:
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv[:1])
    app.setApplicationName("pilas-engine interprete")
    pilas.abrir_interprete(do_raise=True)
else:
    pilas.abrir_asistente()
"""
