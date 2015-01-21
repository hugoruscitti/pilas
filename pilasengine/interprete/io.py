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
        if "Traceback (most" in linea or 'File "<input>", line 1' in linea:
            self.destino.ensureCursorVisible()
            return

        if linea.startswith('  File "'):
            linea = linea.replace("File", "en el archivo")
            linea = linea.replace('line', 'linea')
            linea = linea[:linea.find(', in')]

        if 'NameError' in linea:
            linea = linea.replace('name', 'el nombre').replace('is not defined', 'no existe')

        self.destino.insertar_error(linea.decode('utf-8'))
        self.destino.ensureCursorVisible()

class NormalOutput(Output):
    "Representa la salida estándar de la consola."

    def write(self, linea):
        self.destino.stdout_original.write(linea)
        self.destino.imprimir_linea(linea.decode('utf-8'))
        self.destino.ensureCursorVisible()

        if '<bound method' in linea:
            print "\n\n ... Hey, tal vez olvidaste poner () al final de la anterior sentencia no?"
