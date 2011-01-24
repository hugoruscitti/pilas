# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


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

    def actualizar_simuladores(self):
        self.mundo.tweener.update(16)
        self.mundo.tasks.update(16/1000.0)
        pilas.fisica.fisica.actualizar()

    def actualizar_actores(self):
        for actor in pilas.actores.todos:
            actor.actualizar_comportamientos()
            actor.actualizar_habilidades()
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
    """Representa al mundo pero en pausa, donde se muestra la imagen sin moverse.

    En este modo puedes pulsar la tecla barra espaciadora para avanzar
    un solo cuadro de animación o la tecla derecha para avanzar rápidamente
    en la simulación.

    """

    def __init__(self, m):
        ModoEjecucionNormal.__init__(self, m)
        self.icono = pilas.actores.Actor("icono_pausa.png")
        self.icono.z = -100
        # Hace que no funcione la repreticion de tecla para espacio
        # (asi se puede avanzar la simulacion paso a paso).
        self.pulso_avanzar = False

    def actualizar_simuladores(self):
        pass

    def actualizar_actores(self):
        pass

    def emitir_evento_actualizar(self):
        self.mundo.control.actualizar()

        # Permite avanzar cuadros de animacion rápidamente
        # pulsando la tecla derecha.
        if self.mundo.control.derecha:
            self.actualizar_un_paso()

        # Permite avanzar de a un solo cuadro pulsando
        # la barra espaciadora.
        if self.mundo.control.boton and not self.pulso_avanzar:
            self.actualizar_un_paso()
            self.pulso_avanzar = True
        else:
            if not self.mundo.control.boton:
                self.pulso_avanzar = False


    def actualizar_un_paso(self):
        ModoEjecucionNormal.actualizar_actores(self)
        pilas.eventos.actualizar.send("bucle")

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
        self.pizarra = pilas.actores.Pizarra()
        pilas.eventos.inicia_modo_depuracion.send("ModoEjecucionDepuracion")


    def dibujar_actores(self):

        ModoEjecucionNormal.dibujar_actores(self)

        color_de_colision = pilas.colores.verde_transparente
        color_de_punto_de_control = pilas.colores.rojo_transparente
        color_borde = pilas.colores.gris_transparente
        self.pizarra.limpiar()
        for actor in pilas.actores.todos:
            if actor.radio_de_colision:
                self.pintar_radio_de_colision_del_actor(actor, color_de_colision, color_borde)

            self.pintar_punto_de_control_del_actor(actor, color_de_punto_de_control)

            # intenta dibujar el numero de cuadro que usa el actor
            # si es que tiene una animacion asignada.
            ancho, alto = actor.obtener_area()
            self.pizarra.dibujar_rectangulo(actor.izquierda + 320, 240 - actor.arriba, ancho, alto, False)


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
        pilas.eventos.sale_modo_depuracion.send("ModoEjecucionNormal")
        self.eje.eliminar()
        self.pizarra.eliminar()

    def actualizar_actores(self):
        pilas.eventos.actualiza_modo_depuracion.send("ModoEjecucionDepuracion")
        ModoEjecucionNormal.actualizar_actores(self)


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
