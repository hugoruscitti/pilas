# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import random
import pilas
import math

class Habilidad(object):
    """Representa una habilidad que un actor puede aprender."""

    def __init__(self, receptor):
        self.receptor = receptor

    def actualizar(self):
        pass

    def eliminar(self):
        pass


class RebotarComoPelota(Habilidad):
    """Le indica al actor que rebote y colisiones como una pelota.

    >>> un_actor = pilas.actores.Aceituna()
    >>> un_actor.aprender(pilas.habilidades.RebotarComoPelota)
    """

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        error = random.randint(-10, 10) / 10.0

        circulo = pilas.fisica.Circulo(receptor.x + error,
                                       receptor.y + error,
                                       receptor.radio_de_colision)
        receptor.aprender(pilas.habilidades.Imitar, circulo)
        self.circulo = circulo
        receptor.impulsar = self.impulsar
        receptor.empujar = self.empujar

    def eliminar(self):
        self.circulo.eliminar()

    def impulsar(self, dx, dy):
        self.circulo.impulsar(dx, dy)

    def empujar(self, dx, dy):
        self.circulo.empujar(dx, dy)


class RebotarComoCaja(Habilidad):
    """Le indica al actor que rebote y colisiones como una caja cuadrada.

    >>> un_actor = pilas.actores.Aceituna()
    >>> un_actor.aprender(pilas.habilidades.RebotarComoPelota)
    """

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        error = random.randint(-10, 10) / 10.0
        rectangulo = pilas.fisica.Rectangulo(receptor.x + error,
                                             receptor.y + error,
                                             receptor.radio_de_colision*2 - 4,
                                             receptor.radio_de_colision*2 - 4,
                                             )
        receptor.aprender(pilas.habilidades.Imitar, rectangulo)
        self.rectangulo = rectangulo

    def eliminar(self):
        self.rectangulo.eliminar()


class ColisionableComoPelota(RebotarComoPelota):
    """Le indica al actor que colisione como una pelota, pero que no rebote.

    >>> un_actor = pilas.actores.Aceituna()
    >>> un_actor.aprender(pilas.habilidades.ColisionableComoPelota)
    """

    def __init__(self, receptor):
        RebotarComoPelota.__init__(self, receptor)

    def actualizar(self):
        self.figura.body.position.x = self.receptor.x
        self.figura.body.position.y = self.receptor.y

    def eliminar(self):
        pilas.fisica.fisica.eliminar(self.figura)


class SeguirAlMouse(Habilidad):
    "Hace que un actor siga la posición del mouse en todo momento."

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.escena_actual().mueve_mouse.conectar(self.mover)

    def mover(self, evento):
        self.receptor.x = evento.x
        self.receptor.y = evento.y


class RotarConMouse(Habilidad):
    """"Hace que un actor rote con respecto a la posicion del mouse.

    Ejemplo:

        >>> actor.aprender(pilas.habilidades.RotarConMouse,
                           lado_seguimiento=pilas.habilidades.RotarConMouse.ABAJO)

    """
    ARRIBA = 270
    ABAJO = 90
    IZQUIERDA = 180
    DERECHA = 0

    def __init__(self, receptor, lado_seguimiento=ARRIBA):
        """Inicializa la Habilidad

        :param receptor: La referencia al actor.
        :param lado_seguimiento: Establece el lado del actor que rotará para estar encarado hacia el puntero del mouse.
        """
        Habilidad.__init__(self, receptor)
        pilas.escena_actual().mueve_mouse.conectar(self.se_movio_el_mouse)
        pilas.escena_actual().actualizar.conectar(self.rotar)
        self.lado_seguimiento = lado_seguimiento

        self.raton_x = receptor.x
        self.raton_y = receptor.y

    def se_movio_el_mouse(self, evento):
        self.raton_x = evento.x
        self.raton_y = evento.y

    def rotar(self, evento):

        receptor = (self.receptor.x, self.receptor.y)
        raton = (self.raton_x, self.raton_y)

        angulo = pilas.utils.obtener_angulo_entre(receptor, raton)

        self.receptor.rotacion = -(angulo) - self.lado_seguimiento


class MirarAlActor(Habilidad):
    """"Hace que un actor rote para mirar hacia otro actor.
    """
    ARRIBA = 270
    ABAJO = 90
    IZQUIERDA = 180
    DERECHA = 0

    def __init__(self, receptor, actor_a_seguir, lado_seguimiento=ARRIBA):
        """Inicializa la habilidad.

        :param receptor: Actor que aprenderá la habilidad.
        :param actor_a_seguir : Actor al que se desea seguir con la mirada.
        :param lado_seguimiento: Establece el lado del actor que rotará para estar encarado hacia el actor que desea vigilar.
        """
        Habilidad.__init__(self, receptor)
        pilas.escena_actual().actualizar.conectar(self.rotar)
        self.lado_seguimiento = lado_seguimiento

        self.actor_a_seguir = actor_a_seguir

    def rotar(self, evento):
        receptor = (self.receptor.x, self.receptor.y)
        actor_a_seguir = (self.actor_a_seguir.x, self.actor_a_seguir.y)

        angulo = pilas.utils.obtener_angulo_entre(receptor, actor_a_seguir)

        self.receptor.rotacion = -(angulo) - self.lado_seguimiento


class AumentarConRueda(Habilidad):
    "Permite cambiar el tamaño de un actor usando la ruedita scroll del mouse."

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.escena_actual().mueve_rueda.conectar(self.cambiar_de_escala)

    def cambiar_de_escala(self, evento):
        self.receptor.escala += (evento.delta / 4.0)


class SeguirClicks(Habilidad):
    "Hace que el actor se coloque la posición del cursor cuando se hace click."

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.escena_actual().click_de_mouse.conectar(self.moverse_a_este_punto)

    def moverse_a_este_punto(self, evento):
        if (evento.boton == 1):
            self.receptor.x = [evento.x], 0.5
            self.receptor.y = [evento.y], 0.5


class Arrastrable(Habilidad):
    """Hace que un objeto se pueda arrastrar con el puntero del mouse.

    Cuando comienza a mover al actor se llama al metodo ''comienza_a_arrastrar''
    y cuando termina llama a ''termina_de_arrastrar''. Estos nombres
    de metodos se llaman para que puedas personalizar estos eventos, dado
    que puedes usar polimorfismo para redefinir el comportamiento
    de estos dos metodos. Observa un ejemplo de esto en
    el ejemplo ``pilas.ejemplos.Piezas``.

    """

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        pilas.escena_actual().click_de_mouse.conectar(self.cuando_intenta_arrastrar)

    def cuando_intenta_arrastrar(self, evento):
        "Intenta mover el objeto con el mouse cuando se pulsa sobre el."
        if (evento.boton == 1):
            if self.receptor.colisiona_con_un_punto(evento.x, evento.y):
                pilas.escena_actual().termina_click.conectar(self.cuando_termina_de_arrastrar, id='cuando_termina_de_arrastrar')
                pilas.escena_actual().mueve_mouse.conectar(self.cuando_arrastra, id='cuando_arrastra')
                self.comienza_a_arrastrar()

    def cuando_arrastra(self, evento):
        "Arrastra el actor a la posicion indicada por el puntero del mouse."
        if self._el_receptor_tiene_fisica():
            pilas.escena_actual().fisica.cuando_mueve_el_mouse(evento.x, evento.y)
        else:
            self.receptor.x += evento.dx
            self.receptor.y += evento.dy

    def cuando_termina_de_arrastrar(self, evento):
        "Suelta al actor porque se ha soltado el botón del mouse."
        pilas.escena_actual().mueve_mouse.desconectar_por_id(id='cuando_arrastra')
        self.termina_de_arrastrar()
        pilas.escena_actual().termina_click.desconectar_por_id(id='cuando_termina_de_arrastrar')

    def comienza_a_arrastrar(self):
        if self._el_receptor_tiene_fisica():
            pilas.escena_actual().fisica.capturar_figura_con_el_mouse(self.receptor.figura)

    def termina_de_arrastrar(self):
        if self._el_receptor_tiene_fisica():
            pilas.escena_actual().fisica.cuando_suelta_el_mouse()

    def _el_receptor_tiene_fisica(self):
        return hasattr(self.receptor, 'figura')


class MoverseConElTeclado(Habilidad):
    """Hace que un actor cambie de posición con pulsar el teclado."""
    CUATRO_DIRECCIONES = 4
    OCHO_DIRECCIONES = 8


    def __init__(self, receptor, control=None, direcciones=OCHO_DIRECCIONES, velocidad_maxima=4,
                 aceleracion=1, deceleracion=0.1, con_rotacion=False, velocidad_rotacion=1, marcha_atras=True):
        """Inicializa la habilidad.

        :param receptor: Referencia al actor que aprenderá la habilidad.
        :param control: Control al que va a responder para mover el Actor.
        :param direcciones: Establece si puede mover en cualquier direccion o unicamente en 4 direcciones arriba, abajo, izquierda y derecha. El parametro con_rotacion establece las direcciones a OCHO_DIRECCIONES siempre.
        :param velocidad_maxima: Velocidad maxima en pixeles a la que se moverá el Actor.
        :param aceleracion: Indica lo rapido que acelera el actor hasta su velocidad máxima.
        :param deceleracion: Indica lo rapido que decelera el actor hasta parar.
        :param con_rotacion: Si deseas que el actor rote pulsando las teclas de izquierda y derecha.
        :param velocidad_rotacion: Indica lo rapido que rota un actor sobre si mismo.
        :param marcha_atras: Posibilidad de ir hacia atrás. (True o False)
        """

        Habilidad.__init__(self, receptor)
        pilas.escena_actual().actualizar.conectar(self.on_key_press)

        if control == None:
            self.control = self.receptor.escena.control
        else:
            self.control = control

        self.direcciones = direcciones

        self.velocidad = 0
        self.deceleracion = deceleracion
        self._velocidad_maxima = velocidad_maxima
        self._aceleracion = aceleracion
        self.con_rotacion = con_rotacion
        self.velocidad_rotacion = velocidad_rotacion
        self.marcha_atras = marcha_atras

    def set_velocidad_maxima(self, velocidad):
        self._velocidad_maxima = velocidad

    def get_velocidad_maxima(self):
        return self._velocidad_maxima

    def get_aceleracion(self):
        return self._aceleracion

    def set_aceleracion(self, aceleracion):
        self._aceleracion = aceleracion

    velocidad_maxima = property(get_velocidad_maxima, set_velocidad_maxima, doc="Define la velocidad maxima.")
    aceleracion = property(get_aceleracion, set_aceleracion, doc="Define la acelaracion.")

    def on_key_press(self, evento):

        c = self.control

        if self.con_rotacion:

            if c.izquierda:
                self.receptor.rotacion -= self.velocidad_rotacion * self.velocidad_maxima
            elif c.derecha:
                self.receptor.rotacion += self.velocidad_rotacion * self.velocidad_maxima

            if c.arriba:
                self.avanzar(+1)
            elif c.abajo:
                if self.marcha_atras:
                    self.avanzar(-1)
                else:
                    self.decelerar()
            else:
                self.decelerar()

            rotacion_en_radianes = math.radians(-self.receptor.rotacion + 90)
            dx = math.cos(rotacion_en_radianes) * self.velocidad
            dy = math.sin(rotacion_en_radianes) * self.velocidad
            self.receptor.x += dx
            self.receptor.y += dy

        else:

            if self.direcciones == MoverseConElTeclado.OCHO_DIRECCIONES:
                if c.izquierda:
                    self.receptor.x -= self.velocidad_maxima
                elif c.derecha:
                    self.receptor.x += self.velocidad_maxima

                if c.arriba:
                    self.receptor.y += self.velocidad_maxima
                elif c.abajo:
                    if self.marcha_atras:
                        self.receptor.y -= self.velocidad_maxima
            else:
                if c.izquierda:
                    self.receptor.x -= self.velocidad_maxima
                elif c.derecha:
                    self.receptor.x += self.velocidad_maxima
                elif c.arriba:
                    self.receptor.y += self.velocidad_maxima
                elif c.abajo:
                    if self.marcha_atras:
                        self.receptor.y -= self.velocidad_maxima

    def decelerar(self):
        if self.velocidad > self.deceleracion:
            self.velocidad -= self.deceleracion
        elif self.velocidad < -self.deceleracion:
            self.velocidad += self.deceleracion
        else:
            self.velocidad = 0

    def avanzar(self, delta):
        self.velocidad += self.aceleracion * delta

        if self.velocidad > self.velocidad_maxima:
            self.velocidad = self.velocidad_maxima
        elif self.velocidad < - self.velocidad_maxima / 2:
            self.velocidad = - self.velocidad_maxima / 2


class MoverseComoCoche(MoverseConElTeclado):
    "Hace que un actor se mueva como un coche."

    def __init__(self, receptor, control=None, velocidad_maxima=4,
                 aceleracion=0.06, deceleracion=0.1, rozamiento=0, velocidad_rotacion=1):
        MoverseConElTeclado.__init__(self, receptor,
                                     control=control,
                                     velocidad_maxima=velocidad_maxima,
                                     aceleracion=aceleracion,
                                     deceleracion=deceleracion,
                                     velocidad_rotacion=velocidad_rotacion,
                                     con_rotacion=True)

        self._rozamiento = rozamiento
        self._velocidad_maxima_aux = self.velocidad_maxima

    def set_rozamiento(self, nivel_rozamiento):
        self._rozamiento = nivel_rozamiento
        self.velocidad_maxima = self._velocidad_maxima_aux - self._rozamiento

    def get_rozamiento(self):
        return self._rozamiento

    def set_velocidad_maxima(self, velocidad):
        self._velocidad_maxima = velocidad
        self._velocidad_maxima_aux = self._velocidad_maxima

    def get_velocidad_maxima(self):
        return self.velocidad_maxima

    rozamiento = property(get_rozamiento, set_rozamiento, doc="Define el rozamiento del coche con la superficie por donde circula.")


class PuedeExplotar(Habilidad):
    "Hace que un actor se pueda hacer explotar invocando al metodo eliminar."

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        receptor.eliminar = self.eliminar_y_explotar

    def eliminar_y_explotar(self):
        explosion = pilas.actores.Explosion()
        explosion.x = self.receptor.x
        explosion.y = self.receptor.y
        explosion.escala = self.receptor.escala * 2
        pilas.actores.Actor.eliminar(self.receptor)

class SiempreEnElCentro(Habilidad):
    """Hace que un actor siempre esté en el centro de la camara y la desplace
    cuando el actor se desplaza."""

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)

    def actualizar(self):
        pilas.escena_actual().camara.x = self.receptor.x
        pilas.escena_actual().camara.y = self.receptor.y


class SeMantieneEnPantalla(Habilidad):
    """Se asegura de que el actor regrese a la pantalla si sale o que no
    salga en nigún momento de la pantalla.

    Si el actor sale por la derecha de la pantalla, entonces regresa
    por la izquiera. Si sale por arriba regresa por abajo y asi...

    """
    def __init__(self, receptor, permitir_salida=True):
        """Inicializa la habilidad.

        :param receptor: El actor que aprenderá la habilidad.
        :param permitir_salida: Valor booleano que establece si el actor puede salir por los lados de la ventana y regresar por el lado opuesto. Si se establece a False, el actor no puede salir de la ventana en ningún momento.
        """
        Habilidad.__init__(self, receptor)
        self.ancho, self.alto = pilas.mundo.obtener_area()
        self.permitir_salida = permitir_salida

    def actualizar(self):
        if self.permitir_salida :
            # Se asegura de regresar por izquierda y derecha.
            if self.receptor.derecha < -(self.ancho/2):
                self.receptor.izquierda = (self.ancho/2)
            elif self.receptor.izquierda > (self.ancho/2):
                self.receptor.derecha = -(self.ancho/2)

            # Se asegura de regresar por arriba y abajo.
            if self.receptor.abajo > (self.alto/2):
                self.receptor.arriba = -(self.alto/2)
            elif self.receptor.arriba < -(self.alto/2):
                self.receptor.abajo = (self.alto/2)
        else:
            if self.receptor.izquierda <= -(self.ancho/2):
                self.receptor.izquierda = -(self.ancho/2)
            elif self.receptor.derecha >=  (self.ancho/2):
                self.receptor.derecha = self.ancho/2

            if self.receptor.arriba > (self.alto/2):
                self.receptor.arriba = (self.alto/2)
            elif self.receptor.abajo < -(self.alto/2):
                self.receptor.abajo = -(self.alto/2)


class PisaPlataformas(Habilidad):
    """Enseña al actor a pisar plataformas físicas."""

    def __init__(self, receptor):
        Habilidad.__init__(self, receptor)
        error = random.randint(-10, 10) / 10.0
        self.figura = pilas.fisica.fisica.crear_figura_cuadrado(receptor.x + error,
                                                               receptor.y + error,
                                                               receptor.radio_de_colision,
                                                               masa=10,
                                                               elasticidad=0,
                                                               friccion=0)
        self.ultimo_x = receptor.x
        self.ultimo_y = receptor.y

    def actualizar(self):
        # Mueve el objeto siempre y cuando no parezca que algo
        # no fisico (es decir de pymunk) lo ha afectado.
        self.receptor.x = self.figura.body.position.x
        self.receptor.y = self.figura.body.position.y

    def eliminar(self):
        pilas.fisica.fisica.eliminar(self.figura)


class Imitar(Habilidad):
    "Logra que el actor imite las propiedades de otro."

    def __init__(self, receptor, objeto_a_imitar, con_escala=True, con_rotacion=True):
        """Inicializa la habilidad.

        :param receptor: Referencia al actor.
        :param objeto_a_imitar: Cualquier objeto con atributos rotacion, x e y (por ejemplo otro actor).
        :param con_rotacion: Si debe imitar o no la rotación.
        """
        Habilidad.__init__(self, receptor)
        self.objeto_a_imitar = objeto_a_imitar

        # Establecemos el mismo id para el actor y el objeto fisico
        # al que imita. Así luego en las colisiones fisicas sabremos a que
        # actor corresponde esa colisión.
        receptor.id = objeto_a_imitar.id

        # Y nos guardamos una referencia al objeto físico al que imita.
        # Posterormente en las colisiones fisicas comprobaremos si el
        # objeto tiene el atributo "figura" para saber si estamos delante
        # de una figura fisica o no.
        if hasattr(objeto_a_imitar, '_cuerpo'):
            receptor.figura = objeto_a_imitar

        self.con_escala = con_escala
        self.con_rotacion = con_rotacion

    def actualizar(self):
        self.receptor.x = self.objeto_a_imitar.x
        self.receptor.y = self.objeto_a_imitar.y

        if self.con_escala:
            self.objeto_a_imitar.escala = self.receptor.escala

        if self.con_rotacion:
            self.receptor.rotacion = self.objeto_a_imitar.rotacion

    def eliminar(self):
        if isinstance(self.objeto_a_imitar, pilas.fisica.Figura):
            self.objeto_a_imitar.eliminar()


class Disparar(Habilidad):
    """Establece la habilidad de poder disparar un Actor o un objeto de tipo
    pilas.municion.Municion."""

    def __init__(self, receptor,
                 municion = pilas.actores.Bala,
                 parametros_municion = {},
                 grupo_enemigos=[],
                 cuando_elimina_enemigo=None,
                 frecuencia_de_disparo=10,
                 angulo_salida_disparo=0,
                 offset_disparo=(0,0),
                 offset_origen_actor=(0,0),
                 cuando_dispara=None,
                 escala=1,
                 control=None):
        """
        Construye la habilidad.

        :param municion: Municion o Actor que se disparará.
        :param grupo_enemigos: Actores que son considerados enemigos y con los que colisionará la munición disparada.
        :param cuando_elimina_enemigo: Método que será llamado cuando se produzca un impacto con un enemigo.
        :param frecuencia_de_disparo: El número de disparos por segundo que realizará.
        :param angulo_salida_disparo: Especifica el angulo por donde saldrá el disparo efectuado por el Actor.
        :param offset_disparo: Separación en pixeles (x,y) del disparo con respecto al centro del Actor.
        :param offset_origen_actor: Si el Actor no tiene su origen en el centro, con este parametro podremos colocar correctamente el disparo.
        :param cuando_dispara: Metodo que será llamado cuando se produzca un disparo.
        :param escala: Escala de los actores que serán disparados.
        :param control: Indica los controles que utiliza el actor para saber cuando pulsa el botón de disparar.

        :example:

        >>> mono = pilas.actores.Mono()
        >>> mono.aprender(pilas.habilidades.Disparar,
        >>>               municion=pilas.actores.proyectil.Bala,
        >>>               grupo_enemigos=enemigos,
        >>>               cuando_elimina_enemigo=eliminar_enemigo)

        ..
        """

        Habilidad.__init__(self, receptor)
        self.receptor = receptor

        self._municion = municion
        self.parametros_municion = parametros_municion

        self.offset_disparo_x = offset_disparo[0]
        self.offset_disparo_y = offset_disparo[1]

        self.offset_origen_actor_x = offset_origen_actor[0]
        self.offset_origen_actor_y = offset_origen_actor[1]

        self.angulo_salida_disparo = angulo_salida_disparo
        self.frecuencia_de_disparo = frecuencia_de_disparo
        self.contador_frecuencia_disparo = 0
        self.proyectiles = []

        self.grupo_enemigos = grupo_enemigos

        self.definir_colision(self.grupo_enemigos, cuando_elimina_enemigo)

        self.cuando_dispara = cuando_dispara

        self.escala = escala

        self.control = control

    def set_frecuencia_de_disparo(self, valor):
        self._frecuencia_de_disparo = 60 / valor

    def get_frecuencia_de_disparo(self):
        return self._frecuencia_de_disparo

    def set_municion(self, valor):
        self._municion = valor
        self.parametros_municion = {}

    def get_municion(self):
        return self._municion

    frecuencia_de_disparo = property(get_frecuencia_de_disparo, set_frecuencia_de_disparo, doc="Número de disparos por segundo.")
    municion = property(get_municion, set_municion, doc="Establece el tipo de municion que dispara.")

    def definir_colision(self, grupo_enemigos, cuando_elimina_enemigo):
        self.grupo_enemigos = grupo_enemigos
        pilas.escena_actual().colisiones.agregar(self.proyectiles, self.grupo_enemigos,
                                                 cuando_elimina_enemigo)
    def actualizar(self):
        self.contador_frecuencia_disparo += 1

        if self.pulsa_disparar():
            if self.contador_frecuencia_disparo > self._frecuencia_de_disparo:
                self.contador_frecuencia_disparo = 0
                self.disparar()

        self._eliminar_disparos_innecesarios()

    def _agregar_disparo(self, proyectil):
        proyectil.escala = self.escala
        self._desplazar_proyectil(proyectil, self.offset_disparo_x, self.offset_disparo_y)
        self.proyectiles.append(proyectil)

    def _eliminar_disparos_innecesarios(self):
        for d in list(self.proyectiles):
            if d.esta_fuera_de_la_pantalla():
                d.eliminar()
                self.proyectiles.remove(d)

    def _desplazar_proyectil(self, proyectil, offset_x, offset_y):
        rotacion_en_radianes = math.radians(-proyectil.rotacion)
        dx = math.cos(rotacion_en_radianes)
        dy = math.sin(rotacion_en_radianes)

        proyectil.x += dx * offset_x
        proyectil.y += dy * offset_y

    def disparar(self):
        if (self.receptor.espejado):
            offset_origen_actor_x = -self.offset_origen_actor_x
        else:
            offset_origen_actor_x = self.offset_origen_actor_x

        if issubclass(self.municion, pilas.municion.Municion):

            objeto_a_disparar = self.municion(**self.parametros_municion)

            objeto_a_disparar.disparar(x=self.receptor.x+offset_origen_actor_x,
                                   y=self.receptor.y+self.offset_origen_actor_y,
                                   angulo_de_movimiento=self.receptor.rotacion + -(self.angulo_salida_disparo),
                                   rotacion=self.receptor.rotacion - 90,
                                   offset_disparo_x=self.offset_disparo_x,
                                   offset_disparo_y=self.offset_disparo_y)

            for disparo in objeto_a_disparar.proyectiles:
                self._agregar_disparo(disparo)
                disparo.fijo = self.receptor.fijo

        elif issubclass(self.municion, pilas.actores.Actor):

            objeto_a_disparar = self.municion(x=self.receptor.x+offset_origen_actor_x,
                                              y=self.receptor.y+self.offset_origen_actor_y,
                                              rotacion=self.receptor.rotacion - 90,
                                              angulo_de_movimiento=self.receptor.rotacion + -(self.angulo_salida_disparo))

            self._agregar_disparo(objeto_a_disparar)
            objeto_a_disparar.fijo = self.receptor.fijo
        else:
            raise Exception("No se puede disparar este objeto.")

        if self.cuando_dispara:
            self.cuando_dispara()


    def eliminar(self):
        pass

    def pulsa_disparar(self):
        return self.control.boton if self.control else pilas.escena_actual().control.boton


class DispararConClick(Disparar):
    """Establece la habilidad de poder disparar un Actor o un objeto de tipo
    pilas.municion.Municion pulsando el boton izquierdo del ratón."""

    def __init__(self, *k, **kv):
        super(DispararConClick, self).__init__(*k, **kv)
        self.boton_pulsado = False
        pilas.eventos.click_de_mouse.conectar(self.cuando_hace_click)
        pilas.eventos.termina_click.conectar(self.cuando_termina_click)

    def cuando_hace_click(self, evento):
        if evento.boton == 1:
            self.boton_pulsado = True

    def cuando_termina_click(self, evento):
        if evento.boton == 1:
            self.boton_pulsado = False

    def pulsa_disparar(self):
        return self.boton_pulsado

class PerseguirAOtroActor(Habilidad):
    """Hace que un actor persiga a otro actor.
       No navega alrededor de obstaculos.
    """

    def __init__(self, receptor, objetivo, velocidad=5):
        Habilidad.__init__(self, receptor)
        self.objetivo = objetivo
        self.velocidad = velocidad

    def actualizar(self):

        def limitar(valor):
            return min(max(valor, -self.velocidad), self.velocidad)

        self.receptor.x += limitar(self.objetivo.x - self.receptor.x)
        self.receptor.y += limitar(self.objetivo.y - self.receptor.y)
