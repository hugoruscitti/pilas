# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


class Gestor(object):
    """ Clase que permite el control de las escenas en pilas."""


    def __init__(self):
        self.escenas = []

    def limpiar(self):
        "Elimina todas las escenas del gestor."
        for x in self.escenas:
            x._limpiar()

        self.escenas = []

    def cambiar_escena(self, escena):
        "Define una escena exclusiva y la inicializa (elimina todo lo demas)."
        self.limpiar()
        self.escenas.append(escena)
        escena.iniciar()

    def almacenar_escena(self, escena):
        if self.escena_actual():
            self.escena_actual()._pausar_fisica()
            self.escena_actual().pausar()

        self.escenas.append(escena)
        escena.iniciar()

    def recuperar_escena(self):
        if len(self.escenas) > 1:
            self.escenas[-1]._limpiar()
            escena_actual = self.escenas.pop()
            escena_anterior = self.escenas[-1]
            escena_anterior._reanudar_fisica()
            escena_anterior.reanudar()
        else:
            raise Exception("Debe haber al menos una escena en la pila para restaurar.")

    def escena_actual(self):
        "Retorna la escena actual o None si no hay escena definida."
        if len(self.escenas) > 0:
            return self.escenas[-1]
        else:
            return None

    def actualizar(self):
        escena = self.escena_actual()

        if escena:
            escena.actualizar()
            escena._actualizar_eventos()

            for escena in self.escenas:
                escena._actualizar_fisica()
