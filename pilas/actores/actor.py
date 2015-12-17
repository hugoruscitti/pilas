# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import inspect

import pilas
from pilas import utils
from pilas.estudiante import Estudiante

IZQUIERDA = ["izquierda"]
DERECHA = ["derecha"]
ARRIBA = ["arriba", "superior"]
CENTRO = ["centro", "centrado", "medio", "arriba"]
ABAJO = ["abajo", "inferior", "debajo"]


class Actor(object, Estudiante):
    """Representa un objeto visible en pantalla, algo que se ve y tiene
    posicion.

    .. image:: images/actores/actor.png

    Un objeto Actor se tiene que crear siempre indicando una imagen. Si no
    se especifica una imagen, se verá una pila de color gris cómo la que
    está mas arriba.

    Una forma de crear el actor con una imagen es:

        >>> protagonista = Actor("protagonista_de_frente.png")

    incluso, es equivalente hacer lo siguiente:

        >>> imagen = pilas.imagenes.cargar("protagonista_de_frente.png")
        >>> protagonista = Actor(imagen)

    Luego, una vez que ha sido ejecutada la sentencia aparecerá
    el nuevo actor para que puedas manipularlo. Por ejemplo
    alterando sus propiedades:

        >>> protagonista.x = 100
        >>> protagonista.escala = 2
        >>> protagonista.rotacion = 30

    Estas propiedades también se pueden manipular mediante
    interpolaciones. Por ejemplo, para aumentar el tamaño del
    personaje de 1 a 5 en 7 segundos:

        >>> protagonista.escala = 1
        >>> protagonista.escala = [5], 7

    Si quieres que el actor sea invisible, un truco es crearlo
    con la imagen ``invisible.png``:

        >>> invisible = pilas.actores.Actor('invisible.png')
    """

    def __init__(self, imagen="sin_imagen.png", x=0, y=0):
        """ Constructor del Actor.

        :param imagen: Ruta de la imagen del Actor.
        :type imagen: string
        :param x: Posición horizontal del Actor.
        :type x: int
        :param y: Posición vertical del Actor.
        :type y: int
        """

        if not pilas.mundo:
            mensaje = "Tiene que invocar a la funcion ``pilas.iniciar()`` " \
            "para comenzar."
            print(mensaje)
            raise Exception(mensaje)

        Estudiante.__init__(self)
        self._actor = pilas.mundo.motor.obtener_actor(imagen, x=x, y=y)
        self.centro = ('centro', 'centro')

        self.id = utils.obtener_uuid()

        self.x = x
        self.y = y
        self.transparencia = 0

        # Define en que escena se encuentra el actor.
        self.escena = None

        # Define el nivel de lejanía respecto del observador.
        self.z = 0
        self._espejado = False
        self.radio_de_colision = 10
        pilas.actores.utils.insertar_como_nuevo_actor(self)
        self._transparencia = 0
        self.anexados = []
        self._vivo = True

        # Velocidades horizontal y vertical
        self._vx = 0
        self._vy = 0
        self._dx = self.x
        self._dy = self.y

        # Listas para definir los callbacks de los eventos
        self._callback_cuando_hace_click = set()
        self._callback_cuando_mueve_mouse = set()

    def definir_centro(self, coords):
        """ Define en que posición estará el centro del Actor.

        Se puede definir la posición mediante unas coordenadas numéricas o
        mediante texto.

        La forma de definirlo mediante coordenadas numéricas seria así:

        >>> mi_actor.definir_centro((10,50))

        La otra forma de definirlo mediante texto sería:

        >>> mi_actor.definir_centro(('centro','derecha'))

        :param coords: Tupla de coordenadas horizontal y vertical (x, y) en las
                       que se establecerá el centro del Actor.
        """
        (x, y) = coords
        if type(x) == str:
            if x not in IZQUIERDA + CENTRO + DERECHA:
                raise Exception("No puedes definir '%s' como eje horizontal." %(x))
            x = self._interpretar_y_convertir_posicion(x, self.obtener_ancho())
        if type(y) == str:
            if y not in ARRIBA + CENTRO + ABAJO:
                raise Exception("No puedes definir '%s' como eje vertical." %(y))
            y = self._interpretar_y_convertir_posicion(y, self.obtener_alto())

        self._centro = (x, y)
        self._actor.definir_centro(x, y)

    def _interpretar_y_convertir_posicion(self, posicion, maximo_valor):
        if posicion in IZQUIERDA + ARRIBA:
            return 0
        elif posicion in CENTRO:
            return int(maximo_valor / 2.0)
        elif posicion in DERECHA + ABAJO:
            return maximo_valor
        else:
            raise Exception("El valor '%s' no corresponde a una posicion, use numeros o valores como 'izquierda', 'arriba' etc." %(posicion))

    def obtener_centro(self):
        """ Obtiene las coordenadas del centro del Actor. """
        return self._centro

    centro = property(obtener_centro, definir_centro, doc="""
        Cambia la posición del punto (x, y) dentro de actor.

        Inicialmente, cuando tomamos un actor y definimos sus
        atributos (x, y). Ese punto, será el que representa el centro
        del personaje.

        Eso hace que las rotaciones sean siempre sobre el centro
        del personajes, igual que los cambios de escala y la posición.

        En algunas ocasiones, queremos que el punto (x, y) sea otra
        parte del actor. Por ejemplo sus pies. En esos casos
        es útil definir el centro del actor.

        Por ejemplo, si queremos mover el centro del actor podemos
        usar sentencias cómo estas:

            >>> actor.centro = ("izquierda", "abajo")
            >>> actor.centro = ("centro", "arriba")

        Pulsa la tecla **F8** para ver el centro del los actores
        dentro de pilas. Es aconsejable pulsar la tecla **+** para
        que el punto del modo **F8** se vea bien.
        """)

    def definir_posicion(self, x, y):
        """ Define la posición del Actor en el mundo.

        :param x: Posición horizontal del Actor en el mundo.
        :type x: int
        :param y: Posición vertical del Actor en el mundo.
        :type y: int
        """
        self._actor.definir_posicion(x, y)

    def obtener_posicion(self):
        """ Obtiene la posición del Actor en el mundo. """
        return self._actor.obtener_posicion()

    def dibujar(self, aplicacion):
        """ Metodo interno para el dibujado del Actor en pantalla. """
        self._actor.dibujar(aplicacion)

    def get_x(self):
        x, y = self.obtener_posicion()
        return x

    @pilas.utils.interpolable
    def set_x(self, x):
        self.definir_posicion(x, self.y)

    def get_z(self):
        return self._z

    @pilas.utils.interpolable
    def set_z(self, z):
        self._z = z
        pilas.actores.utils.ordenar_actores_por_valor_z()

    @pilas.utils.interpolable
    def set_y(self, y):
        self.definir_posicion(self.x, y)

    def get_y(self):
        x, y = self.obtener_posicion()
        return y

    @pilas.utils.interpolable
    def set_scale(self, s):
        if s < 0.001:
            s = 0.001

        ultima_escala = self.obtener_escala()

        # Se hace la siguiente regla de 3 simple:
        #
        #  ultima_escala          self.radio_de_colision
        #  s                      ?

        self.definir_escala(s)
        self.radio_de_colision = (s * self.radio_de_colision) / max(ultima_escala, 0.0001)

    @pilas.utils.interpolable
    def set_scale_x(self, s):
        if s < 0.001:
            s = 0.001
        self._actor.definir_escala_x(s)

    @pilas.utils.interpolable
    def set_scale_y(self, s):
        if s < 0.001:
            s = 0.001
        self._actor.definir_escala_y(s)

    def get_scale(self):
        return self.obtener_escala()

    def get_scale_x(self):
        return self._actor._escala_x

    def get_scale_y(self):
        return self._actor._escala_y

    def get_rotation(self):
        return self.obtener_rotacion()

    @pilas.utils.interpolable
    def set_rotation(self, x):
        self.definir_rotacion(x)

    def get_espejado(self):
        return self._espejado

    def set_espejado(self, nuevo_valor):
        if self._espejado != nuevo_valor:
            self._espejado = nuevo_valor
            self._actor.set_espejado(nuevo_valor)

    @pilas.utils.interpolable
    def set_transparencia(self, nuevo_valor):
        self._transparencia = nuevo_valor
        self.definir_transparencia(nuevo_valor)

    def get_transparencia(self):
        return self._transparencia

    def get_imagen(self):
        return self.obtener_imagen()

    def set_imagen(self, imagen):
        if isinstance(imagen, str):
            imagen = pilas.imagenes.cargar(imagen)

        self.definir_imagen(imagen)

    def get_fijo(self):
        return self._actor.fijo

    def set_fijo(self, fijo):
        self._actor.fijo = fijo

    def get_vx(self):
        return self._vx

    def get_vy(self):
        return self._vy

    espejado = property(get_espejado, set_espejado, doc="Indica si se tiene que invertir horizonaltamente la imagen del actor.")
    z = property(get_z, set_z, doc="Define lejania respecto del observador.")
    x = property(get_x, set_x, doc="Define la posición horizontal.")
    y = property(get_y, set_y, doc="Define la posición vertical.")
    vx = property(get_vx, None, doc="Obtiene la velocidad horizontal del actor.")
    vy = property(get_vy, None, doc="Obtiene la velocidad vertical del actor.")
    rotacion = property(get_rotation, set_rotation, doc="Angulo de rotación (en grados, de 0 a 360)")
    escala = property(get_scale, set_scale, doc="Escala de tamaño, 1 es normal, 2 al doble de tamaño etc...)")
    escala_x = property(get_scale_x, set_scale_x, doc="Escala de tamaño horizontal, 1 es normal, 2 al doble de tamaño etc...)")
    escala_y = property(get_scale_y, set_scale_y, doc="Escala de tamaño vertical, 1 es normal, 2 al doble de tamaño etc...)")
    transparencia = property(get_transparencia, set_transparencia, doc="Define el nivel de transparencia, 0 indica opaco y 100 la maxima transparencia.")
    imagen = property(get_imagen, set_imagen, doc="Define la imagen a mostrar.")
    fijo = property(get_fijo, set_fijo, doc="Indica si el actor debe ser independiente a la cámara.")

    def eliminar(self):
        """Elimina el actor de la lista de actores que se imprimen en pantalla."""
        self._eliminar_anexados()
        self.destruir()

    def destruir(self):
        """Elimina a un actor pero de manera inmediata."""
        self._vivo = False
        self.eliminar_habilidades()
        self.eliminar_comportamientos()
        # Solo permite eliminar el actor si está en su escena.
        if self in pilas.escena_actual().actores:
            pilas.escena_actual().actores.remove(self)

    def actualizar(self):
        """Actualiza el estado del actor.

        Este metodo se llama una vez por frame, y generalmente se suele
        usar para implementar el comportamiento del actor.

        Si estás haciendo una subclase de Actor, es aconsejable que re-definas
        este método."""
        pass

    def pre_actualizar(self):
        """Actualiza comportamiento y habilidades antes de la actualización.
        También actualiza la velocidad horizontal y vertical que lleva el actor.
        """
        self.actualizar_comportamientos()
        self.actualizar_habilidades()
        self.__actualizar_velocidad()

    def _agregar_callback(self, grupo_de_callbacks, callback):
        """Agrega una función para invocar en una colección.

        Este método se asegura de agregar funciones que no esperen
        argumentos, o bien, solamente esperen un argumento.

        Si la función a agregar espera un argumento, este método se
        asegura de enviarle el actor receptor del evento.
        """
        cantidad_de_argumentos = len(inspect.getargspec(callback).args)

        if inspect.ismethod(callback):
            cantidad_de_argumentos -= 1

        if cantidad_de_argumentos > 1:
            raise Exception("No puedes asignar una funcion que espera 2 o mas argumentos")
        elif cantidad_de_argumentos == 1:
            # Si la función espera un argumento, se re-define la función para que siempre
            # reciba al actor sobre el que se produjo el evento.

            def inyectar_self(f):
                def invocar():
                    f(self)
                return invocar

            callback = inyectar_self(callback)

        grupo_de_callbacks.add(callback)

    def _ejecutar_callback(self, evento, listado_de_callbacks ):
        """ Ejecuta el listado de métodos asociados a un callback si se
        produce una colisión con el ratón y el actor
        """
        if self.colisiona_con_un_punto(evento.x, evento.y):
            a_eliminar = []
            for callback in set(listado_de_callbacks):
                try:
                    callback()
                except ReferenceError:
                    a_eliminar.append(callback)

            if a_eliminar:
                for x in a_eliminar:
                    try:
                        listado_de_callbacks.remove(x)
                    except:
                        raise ValueError("La funcion no está agregada en el callback")

    def set_cuando_hace_click(self, callback):
        if (callback is None):
            self._callback_cuando_hace_click.clear()
        else:
            pilas.eventos.click_de_mouse.conectar(self._cuando_hace_click)
            self._agregar_callback(self._callback_cuando_hace_click, callback)

    def get_cuando_hace_click(self):
        return self._callback_cuando_hace_click

    def _cuando_hace_click(self, evento):
        self._ejecutar_callback(evento, self._callback_cuando_hace_click)

    cuando_hace_click = property(get_cuando_hace_click, set_cuando_hace_click, doc="")


    def set_cuando_mueve_el_mouse(self, callback):
        if (callback is None):
            self._callback_cuando_mueve_mouse.clear()
        else:
            pilas.eventos.mueve_mouse.conectar(self._cuando_mueve_mouse)
            self._agregar_callback(self._callback_cuando_mueve_mouse, callback)

    def get_cuando_mueve_el_mouse(self):
        return self._callback_cuando_mueve_mouse

    def _cuando_mueve_mouse(self, evento):
        self._ejecutar_callback(evento, self._callback_cuando_mueve_mouse)

    cuando_mueve_el_mouse = property(get_cuando_mueve_el_mouse, set_cuando_mueve_el_mouse, doc="")


    def click_de_mouse(self, callback):
        """Acceso directo para conectar el actor al evento de click_de_mouse.
        No se debe redefinir este método."""
        pilas.eventos.click_de_mouse.conectar(callback)

    def mueve_mouse(self, callback):
        """Acceso directo para conectar el actor al evento de mueve_mouse.
        No se debe redefinir este método."""
        pilas.eventos.mueve_mouse.conectar(callback)

    def mueve_camara(self, callback):
        """Acceso directo para conectar el actor al evento de mueve_camara.
        No se debe redefinir este método."""
        pilas.eventos.mueve_camara.conectar(callback)

    def termina_click(self, callback):
        """Acceso directo para conectar el actor al evento de termina_click.
        No se debe redefinir este método."""
        pilas.eventos.termina_click.conectar(callback)

    def mueve_rueda(self, callback):
        """Acceso directo para conectar el actor al evento de mueve_rueda.
        No se debe redefinir este método."""
        pilas.eventos.mueve_rueda.conectar(callback)

    def pulsa_tecla(self, callback):
        """Acceso directo para conectar el actor al evento de pulsa_tecla.
        No se debe redefinir este método."""
        pilas.eventos.pulsa_tecla.conectar(callback)

    def suelta_tecla(self, callback):
        """Acceso directo para conectar el actor al evento de suelta_tecla.
        No se debe redefinir este método."""
        pilas.eventos.suelta_tecla.conectar(callback)

    def pulsa_tecla_escape(self, callback):
        """Acceso directo para conectar el actor al evento de pulsa_tecla_escape.
        No se debe redefinir este método."""
        pilas.eventos.pulsa_tecla_escape.conectar(callback)

    def __actualizar_velocidad(self):
        """ Calcula la velocidad horizontal y vertical del actor. """

        if (self._dx != self.x):
            self._vx = abs(self._dx - self.x)
            self._dx = self.x
        else:
            self._vx = 0

        if (self._dy != self.y):
            self._vy = abs(self._dy - self.y)
            self._dy = self.y
        else:
            self._vy = 0

    def __cmp__(self, otro_actor):
        """Compara dos actores para determinar cual esta mas cerca de la camara.

        Este metodo se utiliza para ordenar los actores antes de imprimirlos
        en pantalla. De modo tal que un usuario pueda seleccionar que
        actores se ven mas arriba de otros cambiando los valores de
        los atributos `z`."""

        if otro_actor.z >= self.z:
            return 1
        else:
            return -1

    def get_izquierda(self):
        return self.x - (self.centro[0] * self.escala)

    @pilas.utils.interpolable
    def set_izquierda(self, x):
        self.x = x + (self.centro[0] * self.escala)

    izquierda = property(get_izquierda, set_izquierda, doc="Establece el " \
                         "espacio entre la izquierda del actor y el centro " \
                         "de coordenadas del mundo.")

    def get_derecha(self):
        return self.izquierda + self.obtener_ancho() * self.escala

    @pilas.utils.interpolable
    def set_derecha(self, x):
        self.set_izquierda(x - (self.ancho * self.escala))

    derecha = property(get_derecha, set_derecha, doc="Establece el " \
                         "espacio entre la derecha del actor y el centro " \
                         "de coordenadas del mundo.")

    def get_abajo(self):
        return self.get_arriba() - self.alto * self.escala

    @pilas.utils.interpolable
    def set_abajo(self, y):
        self.set_arriba(y + (self.alto * self.escala))

    abajo = property(get_abajo, set_abajo, doc="Establece el " \
                         "espacio entre la parte inferior del actor y el " \
                         "centro de coordenadas del mundo.")

    def get_arriba(self):
        return self.y + (self.centro[1] * self.escala)

    @pilas.utils.interpolable
    def set_arriba(self, y):
        self.y = y - (self.centro[1] * self.escala)

    arriba = property(get_arriba, set_arriba, doc="Establece el " \
                         "espacio entre la parte superior del actor y el " \
                         "centro de coordenadas del mundo.")

    def colisiona_con_un_punto(self, x, y):
        """Determina si un punto colisiona con el area del actor.

        Todos los actores tienen un area rectangular, pulsa la
        tecla **F10** para ver el area de colision.
        Si el actor tiene la propiedad fijo en True, el cálculo
        se hace independientemente de la cámara.

        :param x: Posición horizontal del punto.
        :type x: int
        :param y: Posición vertical del punto.
        :type y: int
        """
        if self.fijo:
            x = x - pilas.escena_actual().camara.x
            y = y - pilas.escena_actual().camara.y
        return self.izquierda <= x <= self.derecha and self.abajo <= y <= self.arriba

    def distancia_con(self, otro_actor):
        """Determina la distancia con el ``otro_actor``

        :param otro_actor: El otro actor para ver la distancia
        :type otro_actor: pilas.actores.Actor

        """
        return utils.distancia_entre_dos_actores(self, otro_actor)

    def actor_mas_cercano(self):
        """Retorna otro actor mas cercano a este actor"""
        return utils.actor_mas_cercano_al_actor(self)

    def distancia_al_punto(self, x, y):
        """Determina la distancia desde el centro del actor hasta el punto
        determinado

        Todos los actores tienen un area rectangular, pulsa la
        tecla **F10** para ver el area de colision.

        :param x: Posición horizontal del punto.
        :type x: int
        :param y: Posición vertical del punto.
        :type y: int
        """
        return utils.distancia_entre_dos_puntos((self.x, self.y), (x, y))

    def colisiona_con(self, otro_actor):
        """Determina si este actor colisiona con ``otro_actor``

        :param otro_actor: El otro actor para verificar si colisiona.
        :type otro_actor: pilas.actores.Actor

        """
        return utils.colisionan(self, otro_actor)

    def obtener_rotacion(self):
        return self._actor.obtener_rotacion()

    def definir_rotacion(self, r):
        r = r % 360
        self._actor.definir_rotacion(r)

    def definir_color(self, c):
        self._actor.definir_color(c)

    def obtener_imagen(self):
        """ Obtinene la imagen del Actor. """
        return self._actor.obtener_imagen()

    def definir_imagen(self, imagen):
        """ Define la imagen del Actor y establece el centro del mismo a
        ('centro,'centro').

        :param imagen: Ruta de la imagen del Actor.
        :type imagen: string
        """
        self._actor.definir_imagen(imagen)
        self.centro = ('centro', 'centro')

    def duplicar(self, **kv):
        """ Duplica un Actor.

        :return: `Actor`.
        """
        duplicado = self.__class__()

        for clave in kv:
            setattr(duplicado, clave, kv[clave])

        return duplicado

    def obtener_ancho(self):
        return self.imagen.ancho()

    def obtener_alto(self):
        return self.imagen.alto()

    ancho = property(obtener_ancho, doc="Obtiene el ancho del Actor.")
    alto = property(obtener_alto, doc="Obtiene el alto del Actor.")

    def __mul__(self, cantidad):
        if type(cantidad) is not int or cantidad < 1:
            raise TypeError("Solo puede multiplicar por numeros enteros " \
                            "mayores a 1.")

        grupo = pilas.atajos.fabricar(self.__class__, cantidad - 1)
        grupo.append(self)
        return grupo

    def __str__(self):
        return "<%s en (%d, %d)>" % (self.__class__.__name__, self.x, self.y)

    def obtener_escala(self):
        return self._actor.obtener_escala()

    def definir_escala(self, escala):
        self._actor.definir_escala(escala)

    def definir_transparencia(self, valor):
        self._actor.definir_transparencia(valor)

    def imitar(self, otro_actor_o_figura, *args, **kwargs):
        """ Hace que un Actor copie la posición y la rotación de otro Actor o
        Figura fisica.

        Por ejemplo:

        >>> circulo_dinamico = pilas.fisica.Circulo(10, 200, 50)
        >>> mi_actor.imitar(circulo_dinamico)

        :param otro_actor_o_figura: Actor o Figura física a imitar.
        :type otro_actor_o_figura: `Actor`, `Figura`
        """
        self.aprender(pilas.habilidades.Imitar, otro_actor_o_figura, *args, **kwargs)

    def decir(self, mensaje, autoeliminar=True):
        """Emite un mensaje usando un globo similar al de los comics.

        :param mensaje: Texto a mostrar en el mensaje.
        :type mensaje: string
        :param autoeliminar: Establece si se eliminará el globo al cabo de unos segundos.
        :type autoeliminar: boolean
        """
        nuevo_actor = pilas.actores.Globo(mensaje, self.x, self.y, autoeliminar=autoeliminar)
        nuevo_actor.aprender(pilas.habilidades.Imitar, self, False)
        nuevo_actor.z = self.z - 1
        self.anexar(nuevo_actor)
        pilas.atajos.leer(mensaje)

    def anexar(self, otro_actor):
        """ Agrega un Actor a la lista de actores anexados al Actor actual.
        Cuando se elimina un Actor, se eliminan los actores anexados.

        :param otro_actor: Actor a anexar.
        :type otro_actor: `Actor`
        """
        self.anexados.append(otro_actor)

    def _eliminar_anexados(self):
        for x in self.anexados:
            x.eliminar()

    def esta_fuera_de_la_pantalla(self):
        """Indica si el actor está fuera del area visible de la pantalla.

        :return: boolean"""
        if self.fijo:
            return False
        izquierda, derecha, arriba, abajo = self.escena.camara.obtener_area_visible()
        return self.derecha < izquierda or self.izquierda > derecha or self.abajo > arriba or self.arriba < abajo

    def es_fondo(self):
        """ Comprueba si el actor es un fondo del juego.

        :return: boolean"""
        return False
