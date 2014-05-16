# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

class Output(object):
    "Representación abstracta de un archivo de salida de datos."

    def __init__(self, destino):
        self.destino = destino

class ErrorOutput(Output):
    "Representa la salida de error en la consola."

    def write(self, linea):
        self.destino.stdout_original.write(linea)

        # Solo muestra el error en consola si es un mensaje util.
        if linea.startswith('Traceback (most re') or linea.startswith('  File "<input>", line 1, in'):
            pass
        else:

            if linea.startswith('  File "'):
                linea = linea.replace("File", "Archivo").replace('line', 'linea')
                linea = linea[:linea.find(', in')] + " ..."

            self.destino.insertar_error(linea.decode('utf-8'))

        self.destino.ensureCursorVisible()

class NormalOutput(Output):
    "Representa la salida estándar de la consola."

    def write(self, linea):
        self.destino.stdout_original.write(linea)
        self.destino.imprimir_linea(linea.decode('utf-8'))
        self.destino.ensureCursorVisible()