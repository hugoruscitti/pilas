# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


class Gestor(object):
    """Clase que permite el control de las escenas en pilas."""

    def __init__(self):
        self.escenas = []

    def limpiar(self):
        """Elimina todas las escenas del gestor."""
        for x in self.escenas:
            x._limpiar()

        self.escenas = []

    def cambiar_escena(self, escena):
        """Define una escena unica y la inicializa.

        Las escenas que estuvieran apiladas se eliminan.

        :param escena: Escena a la que se quiere cambiar."""

        self.limpiar()
        self.escenas.append(escena)
        escena.camara.reiniciar()
        escena.iniciar()
        escena.iniciada = True

    def almacenar_escena(self, escena):
        """Pausa la escena actualmente activa e inicializa la escena que
        le pasamos como parametro.

        :param escena: Escena que deseamos que sea la activa.
        """
        if self.escena_actual():
            self.escena_actual()._pausar_fisica()
            self.escena_actual().guardar_posicion_camara()
            self.escena_actual().pausar()

        self.escenas.append(escena)
        escena.camara.reiniciar()
        escena.iniciar()
        escena.iniciada = True

    def recuperar_escena(self):
        """Recupera la escena que fue Pausada mediante **almacenar_escena**.
        """
        if len(self.escenas) > 1:
            self.escenas[-1]._limpiar()
            escena_actual = self.escenas.pop()
            escena_anterior = self.escenas[-1]
            escena_anterior._reanudar_fisica()
            escena_anterior.recuperar_posicion_camara()
            escena_anterior.control.limpiar()
            escena_anterior.reanudar()
        else:
            raise Exception("Debe haber al menos una escena en la pila para restaurar.")

    def escena_actual(self):
        """Retorna la escena actual o None si no hay escena definida."""
        if len(self.escenas) > 0:
            return self.escenas[-1]
        else:
            return None

    def actualizar(self):
        escena = self.escena_actual()

        if escena:
            if escena.iniciada:
                escena._actualizar_eventos()

            for escena in self.escenas:
                escena._actualizar_fisica()
