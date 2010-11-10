# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import time

import pilas
import pilas.actores

class ModoEjecucion:
    """Representa un modo de ejecucion del mundo.

    Este objeto representa la estrategia que el mundo tiene
    en un momento particular. Esta abstraccion sirve para
    implementar los modos 'pausa' y 'depuracion' principalmente.
    """

    def __init__(self, mundo):
        self.mundo = mundo

    def alternar_modo_depuracion(self):
        raise Exception("Tiene que redefinir este metodo.")

    def alternar_pausa(self):
        raise Exception("Tiene que redefinir este metodo.")


class ModoEjecucionNormal(ModoEjecucion):
    """Representa al mundo cuando el usuario está jugando normalmente."""

    def esperar(self):
        time.sleep(0.01)

    def actualizar_simuladores(self):
        self.mundo.tweener.update(16)
        self.mundo.tasks.update(16/1000.0)
        pilas.fisica.fisica.actualizar()


    def actualizar_actores(self):
        for actor in pilas.actores.todos:
            actor.actualizar()

    def dibujar_actores(self):
        # Separo el dibujado de los actores porque la lista puede cambiar
        # dutante la actualizacion de actores (por ejemplo si uno se elimina).
        for actor in pilas.actores.todos:
            actor.dibujar(self.mundo.ventana)

    def emitir_evento_actualizar(self):
        self.mundo.control.actualizar()
        pilas.eventos.actualizar.send("bucle")

    def salir(self):
        pass

    def analizar_colisiones(self):
        pilas.colisiones.verificar_colisiones()

    def alternar_modo_depuracion(self):
        self.mundo.definir_modo_ejecucion(ModoEjecucionDepuracion(self.mundo))

    def alternar_pausa(self):
        self.mundo.definir_modo_ejecucion(ModoEjecucionPausado(self.mundo))

class ModoEjecucionPausado(ModoEjecucionNormal):
    """Representa al mundo pero en pausa, donde se muestra la imagen sin moverse."""

    def __init__(self, m):
        ModoEjecucionNormal.__init__(self, m)
        self.icono = pilas.actores.Actor("icono_pausa.png")
        self.icono.z = -100

    def actualizar_simuladores(self):
        pass

    def actualizar_actores(self):
        pass

    def emitir_evento_actualizar(self):
        pass

    def alternar_modo_depuracion(self):
        self.mundo.definir_modo_ejecucion(ModoEjecucionDepuracionPausado(self.mundo))

    def alternar_pausa(self):
        self.mundo.definir_modo_ejecucion(ModoEjecucionNormal(self.mundo))

    def salir(self):
        self.icono.eliminar()

class ModoEjecucionDepuracion(ModoEjecucionNormal):
    """Es el modo de ejecucion normal pero mostrando informacion para desarrolladores."""

    def __init__(self, m):
        import pilas.actores
        ModoEjecucionNormal.__init__(self, m)
        self.eje = pilas.actores.Ejes()

    def salir(self):
        self.eje.eliminar()

    def dibujar_actores(self):

        ModoEjecucionNormal.dibujar_actores(self)

        color_de_colision = pilas.colores.verde_transparente
        color_de_punto_de_control = pilas.colores.rojo_transparente
        color_borde = pilas.colores.gris_transparente

        for actor in pilas.actores.todos:
            if actor.radio_de_colision:
                self.pintar_radio_de_colision_del_actor(actor, color_de_colision, color_borde)

            self.pintar_punto_de_control_del_actor(actor, color_de_punto_de_control)

            # intenta dibujar el numero de cuadro que usa el actor
            # si es que tiene una animacion asignada.

            '''
            try:
                cuadro = actor.animacion.obtener_cuadro()
                self.pintar_numero(cuadro, actor.x, actor.y)
            except AttributeError, e:
                pass
            '''

    def pintar_numero(self, numero, x, y):
        numero = pilas.actores.Texto(str(numero))
        numero.x = x
        numero.y = y

        self.mundo.ventana.Draw(numero)
        numero.eliminar()


    def pintar_radio_de_colision_del_actor(self, actor, color, color_borde):
        x, y = actor.x, actor.y
        radio = actor.radio_de_colision * 2
        pilas.motor.dibujar_circulo(x, y, radio, color, color_borde)

    def pintar_punto_de_control_del_actor(self, actor, color):
        x, y = actor.x, actor.y
        pilas.motor.dibujar_circulo(x, y, 3, color, color)

    def alternar_modo_depuracion(self):
        self.mundo.definir_modo_ejecucion(ModoEjecucionNormal(self.mundo))

    def alternar_pausa(self):
        self.mundo.definir_modo_ejecucion(ModoEjecucionDepuracionPausado(self.mundo))

    def salir(self):
        self.eje.eliminar()


        

class ModoEjecucionDepuracionPausado(ModoEjecucionPausado, ModoEjecucionDepuracion):

    def __init__(self, m):
        ModoEjecucionPausado.__init__(self, m)
        ModoEjecucionDepuracion.__init__(self, m)

    def dibujar_actores(self):
        ModoEjecucionDepuracion.dibujar_actores(self)

    def salir(self):
        ModoEjecucionPausado.salir(self)
        ModoEjecucionDepuracion.salir(self)

    def actualizar_actores(self):
        pass

    def alternar_modo_depuracion(self):
        self.mundo.definir_modo_ejecucion(ModoEjecucionPausado(self.mundo))

    def alternar_pausa(self):
        self.mundo.definir_modo_ejecucion(ModoEjecucionDepuracion(self.mundo))
