# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor


class Temporizador(Actor):
    """Representa un contador de tiempo con cuenta regresiva.

    Por ejemplo:

        >>> t = pilas.actores.Temporizador()
        >>> def hola_mundo():
        ...     pilas.avisar("Hola mundo, pasaron 10 segundos...")
        ...
        >>> t.ajustar(10, hola_mundo)
        >>> t.comenzar()

    """
    
    def iniciar(self, x=0, y=0):
        """Inicia el contador de tiempo con la función indicada."""
        self.imagen = "invisible.png"
        self.texto = self.pilas.actores.Texto("0")
        
        self.tiempo = -1
        self.tiempo_inicial = None
        self.tarea_en_curso = None
        self.funcion_a_invocar = None
        
        self.ajustar(10)
        
    def comenzar(self):
        self.tiempo = self.tiempo_inicial
        self.tarea_en_curso = self.pilas.tareas.siempre(1, self._restar_a_contador)
        
    def detener(self):
        if self.tarea_en_curso:
            self.tarea_en_curso.eliminar()
            self.tarea_en_curso = None
    
    def reiniciar(self):
        self.detener()
        self.comenzar()
        
    def definir_tiempo_texto(self, variable):
        """Define el texto a mostrar en el temporizador.

        :param variable: La cadena de texto a mostrar.
        """
        self.texto.definir_texto(str(variable))

    def _restar_a_contador(self):
        if self.tiempo != 0:
            self.tiempo -= 1
            self.definir_tiempo_texto(self.tiempo)
        else:
            self.detener()
            if self.funcion_a_invocar:
                self.funcion_a_invocar()

    def ajustar(self, tiempo=1, funcion=None):
        """Indica una funcion para ser invocada en el tiempo indicado.

        La función no tiene que recibir parámetros, y luego de
        ser indicada se tiene que iniciar el temporizador.
        """
        self.tiempo_inicial = tiempo
        self.definir_tiempo_texto(tiempo)
        self.funcion_a_invocar = funcion
