# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Dialogo(Actor):
    """
        Representa una secuencia de mensajes entre varios actores.

        >>> mono = pilas.actores.Mono()
        >>> mono2 = pilas.actores.Mono()
        >>> dialogo = pilas.actores.Dialogo()
        >>> dialogo.decir(mono, "Hola Mundo")
        >>> dialogo.decir(mono2, "Estoy diciendo algo")
        >>> dialogo.comenzar()

        .. image:: ../../pilas/data/manual/imagenes/actores/mono_dice.png


    """

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        if getattr(self, 'dialogo', None):
            raise Exception("Ya se ha iniciado el actor, quisiste escribir 'comenzar' en realidad?")

        self.imagen = "invisible.png"
        self.dialogo = []
        self.dialogo_actual = None
        self.modo_automatico = True

    def decir(self, actor, texto):
        """ Añade un texto a la conversación y establece el actor que lo dice.

        :param actor: Actor que dirá el texto.
        :type actor: Actor
        :param texto: Texto que dirá el actor.
        :type texto: string
        """
        self.dialogo.append((actor, texto))

    def decir_inmediatamente(self, actor, texto):
        """ Muestra un texto de dialogo inmediatamente sin seguir una secuencia de dialogo.

        :param actor: Actor que dirá el texto.
        :type actor: Actor
        :param texto: Texto que dirá el actor.
        :type texto: string
        """
        self.dialogo = []
        self._eliminar_dialogo_actual()
        self.decir(actor, texto)
        siguiente = self.obtener_siguiente_dialogo_o_funcion()
        self._mostrar_o_ejecutar_siguiente(siguiente)

    def elegir(self, actor, texto, opciones, funcion_a_invocar):
        """ Muestra un texto de dialogo con una lista de opciones para poder seleccionar y ejecutar una accion cuando se seleccione una de las opciones del cuadro de dialogo.

        :param actor: Actor que dirá el texto.
        :type actor: Actor
        :param texto: Texto que aparecerá en la parte superior del dialogo de opciones.
        :type texto: string
        :param opciones: Array de posibles opciones que mostrará el cuadrio de dialogo.
        :type opciones: Array
        :param funcion_a_invocar: Método al que se llamará cuando se seleccione una de las opciones del listado. Este metodo recibirá como parámetro la opción que se haya seleccinado.

        >>> def cuando_responde_color_favorito(respuesta):
        >>>    colores = {
        >>>               'rojo': pilas.colores.rojo,
        >>>               'verde': pilas.colores.verde,
        >>>               'azul': pilas.colores.azul,
        >>>              }
        >>>
        >>>    pilas.fondos.Color(colores[respuesta])
        >>>    mono.sonreir()
        >>>    d.decir(mono, '¡mira!')
        >>>
        >>> d.elegir(mono_chiquito, 'Mi color favorito es el...', ['rojo', 'verde', 'azul'], cuando_responde_color_favorito)

        """
        self.dialogo.append((actor, texto, opciones, funcion_a_invocar))

    def ejecutar(self, funcion):
        self.dialogo.append(funcion)

    def comenzar(self):
        """ Inicia el dialogo que se haya definido.

            >>> d = pilas.actores.Dialogo()
            >>> d.decir(mono, "¿Cual es tu color favorito?")
            >>> d.comenzar()

        """
        self.avanzar_al_siguiente_dialogo()

    def obtener_siguiente_dialogo_o_funcion(self):
        if self.dialogo:
            return self.dialogo.pop(0)

    def _eliminar_dialogo_actual(self):
        if self.dialogo_actual:
            self.dialogo_actual.eliminar()
            self.dialogo_actual = None

    def _mostrar_o_ejecutar_siguiente(self, siguiente):
        if isinstance(siguiente, tuple):
            # Es un mensaje de dialogo simple
            if len(siguiente) == 2:
                actor, texto = siguiente
                self.dialogo_actual = self.pilas.actores.Globo(texto, dialogo=self, avance_con_clicks=self.modo_automatico)
            else:
                # Es un mensaje con seleccion.
                actor, texto, opciones, funcion_a_invocar = siguiente
                self.dialogo_actual = self.pilas.actores.GloboElegir(texto, opciones, funcion_a_invocar, dialogo=self)

            self.dialogo_actual.colocar_origen_del_globo(actor.x, actor.arriba)
        else:
            siguiente()
            self.avanzar_al_siguiente_dialogo()

    def avanzar_al_siguiente_dialogo(self, evento=None):
        self._eliminar_dialogo_actual()
        siguiente = self.obtener_siguiente_dialogo_o_funcion()

        if siguiente:
            self._mostrar_o_ejecutar_siguiente(siguiente)
        else:
            return False

        return True
