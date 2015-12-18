# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#


import inspect

import pilasengine
from estudiante import Estudiante
from __builtin__ import True

IZQUIERDA = ["izquierda"]
DERECHA = ["derecha"]
ARRIBA = ["arriba", "superior"]
CENTRO = ["centro", "centrado", "medio", "arriba"]
ABAJO = ["abajo", "inferior", "debajo"]

class ActorEliminadoException(Exception):
    pass

class ActorEliminado(object):
    """Representa a un actor que ha sido eliminado y ya no se puede usar.

    Esta clase entra en acción cuando se toma cualquier actor
    y se lo elimina. Cualquier actor de pilas, al momento de ser
    eliminado, cambia de clase y pasa a formar parte de esta
    clase.

    Observá el método '_destruir' de la clase actor.
    """

    def __getattr__(self, *k, **kw):
        plantilla = "Este actor (ex: %s id: %d) ya ha sido eliminado, no se puede utilizar."
        mensaje = plantilla % (self.nombre_de_clase, self.identificador)
        print mensaje
        # raise ActorEliminadoException(mensaje)

    def esta_eliminado(self):
        return True

    def __cmp__(self, otro_actor):
        return 1

    def eliminar(self):
        pass

    def _eliminar_anexados(self):
        pass



class Actor(Estudiante):
    """Representa un objeto visible en pantalla, algo que se ve y tiene
    posicion.

    .. image:: ../../pilas/data/manual/imagenes/actores/actor.png

    Un objeto Actor se tiene que crear siempre indicando una imagen. Si no
    se especifica una imagen, se verán los signos de interrogación de
    color rojo.


    Una forma de crear el actor con una imagen es:

        >>> protagonista = Actor("planeta_azul.png")

    incluso, es equivalente hacer lo siguiente:

        >>> imagen = pilas.imagenes.cargar("planeta_azul.png")
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

    def __init__(self, pilas=None, *k, **kv):
        # Especifica la composión de dibujado (ver actor particula.py).
        self.composicion = None

        if not pilas:
            mensaje = "Ten cuidado, antes de crear un actor tienes que vincularlo con: 'pilas.actores.vincular(MiActor)'"
            raise Exception(mensaje)

        if not isinstance(pilas, pilasengine.Pilas):
            mensaje = "Tienes que enviar el objeto 'pilas' como argumento al actor, en lugar de eso llego esto: " + str(pilas)
            raise Exception(mensaje)

        self.pilas = pilas
        self.padre = None

        if 'x' in kv:
            x = kv['x']
        else:
            x = 0

        if 'y' in kv:
            y = kv['y']
        else:
            y = 0

        if 'imagen' in kv:
            imagen = kv['imagen']
        else:
            imagen = 'sin_imagen.png'

        Estudiante.__init__(self)

        self._definir_valores_iniciales(pilas, x, y, imagen)
        self.etiquetas = pilasengine.etiquetas.Etiquetas()
        self.etiquetas.agregar(self.__class__.__name__)

        # Listas para definir los callbacks de los eventos
        self._callback_cuando_hace_click = set()
        self._callback_cuando_mueve_mouse = set()
        self._grupos_a_los_que_pertenece = []
        self._actores = []

        # Argumentos adicionales.
        self.argumentos_adicionales = (k, kv)

        # Vincula el actor con la escena actual.
        pilas.actores.agregar_actor(self)

    def pre_iniciar(self, x=0, y=0, imagen="sin_imagen.png"):
        """Ejecuta el código inicial del actor.

        Este método se llama automáticamente cuando el actor se
        genera y agrega dentro de una escena.
        """
        if not isinstance(x, (int, long, float)):
            mensaje = "El parametro x tiene un valor no permitido: " + str(x)
            raise Exception(mensaje)
        else:
            self.x = x

        if not isinstance(y, (int, long, float)):
            mensaje = "El parametro y tiene un valor no permitido: " + str(y)
            raise Exception(mensaje)
        else:
            self.y = y

        self.imagen = imagen

    def iniciar(self, *k, **kw):
        pass

    def agregar(self, actor):
        self._actores.append(actor)
        actor.padre = self

    def agregar_al_grupo(self, grupo):
        self._grupos_a_los_que_pertenece.append(grupo)

    def eliminar_del_grupo(self, grupo):
        self._grupos_a_los_que_pertenece.remove(grupo)

    def obtener_cantidad_de_grupos_al_que_pertenece(self):
        return len(self._grupos_a_los_que_pertenece)

    def _definir_valores_iniciales(self, pilas, x, y, imagen=None):
        self.imagen = imagen if imagen else "sin_imagen.png"
        self.x = x
        self.y = y
        self.z = 0
        self.rotacion = 0
        self.escala_x = 1
        self.escala_y = 1
        self.transparencia = 0
        self.espejado = False
        self.fijo = False
        self._figura_de_colision = None

        if imagen:
            self.imagen = imagen

        self.id = pilas.utils.obtener_uuid()

        # Define en que escena se encuentra el actor.
        # self.escena = None
        # Define el nivel de lejanía respecto del observador.

        self.radio_de_colision = 10
        self.anexados = []
        self._vivo = True
        # Velocidades horizontal y vertical
        self._vx = 0
        self._vy = 0
        self._dx = self.x
        self._dy = self.y

    def obtener_figura_de_colision(self):
        return self._figura_de_colision

    def definir_figura_de_colision(self, figura):
        # Elimina la habilidad de imitar si la figura de colision es el objetivo.
        if self.esta_imitando_su_figura():
            self.eliminar_habilidad(self.pilas.habilidades.Imitar)

        if self._figura_de_colision:
            self._figura_de_colision.actor_que_representa_como_area_de_colision = None
            self._figura_de_colision.eliminar()

        self._figura_de_colision = figura
        self._figura_de_colision_dx = 0
        self._figura_de_colision_dy = 0


        if figura:
            figura.actor_que_representa_como_area_de_colision = self

    figura_de_colision = property(obtener_figura_de_colision, definir_figura_de_colision)

    def esta_imitando_su_figura(self):
        if self.tiene_habilidad(self.pilas.habilidades.Imitar):
            if self.habilidades.Imitar.objeto_a_imitar == self.figura_de_colision:
                return True

        return False

    def actualizar(self):
        """Método de actualización lógico del actor.

        Este método se llama automáticamente 60 veces por segundo, es
        donde se puede colocar lógica de actualización y temporizadores.
        """
        pass

    def terminar(self):
        """Se ejecuta justo antes de eliminar el actor de la escena."""
        pass

    def dibujar(self, painter):
        """Pinta el personaje sobre la ventana.

        Este método es interno, se invoca automáticamente desde el
        bucle de pilas-engine.
        """
        escala_x, escala_y = self.escala_x, self.escala_y

        if self._espejado:
            escala_x *= -1

        if not self.fijo:
            dx = self.pilas.obtener_escena_actual().camara.x
            dy = self.pilas.obtener_escena_actual().camara.y
        else:
            dx = 0
            dy = 0

        x = self.x - dx
        y = self.y - dy
        painter.save()

        # Tranformaciones para aplicar al actor

        dx, dy = self.centro
        painter.translate(x, -y)
        painter.rotate(-self.rotacion)
        painter.scale(escala_x, escala_y)
        painter.translate(-dx, -dy)

        if self.transparencia:
            painter.setOpacity(1 - self.transparencia / 100.0)

        # Dibujado de los subactores.
        for un_actor in self._actores:
            un_actor.dibujar(painter)

        self.imagen.dibujar(painter, self.composicion)

        # Vuelve al punto inicial para dibujar el
        # modo depuración.
        painter.translate(dx, dy)

        self.pilas.depurador.cuando_dibuja_actor(self, painter)

        painter.restore()
        painter.save()

        painter.translate(x, -y)
        self.pilas.depurador.cuando_dibuja_actor_sin_transformacion(self, painter)
        painter.restore()

    # # Métodos internos
    def _obtener_imagen(self):
        return self._imagen

    def _definir_imagen(self, imagen_o_ruta):
        if isinstance(imagen_o_ruta, str):
            imagen = self.pilas.imagenes.cargar(imagen_o_ruta)
        else:
            imagen = imagen_o_ruta

        self._imagen = imagen
        self.centro = ("centro", "centro")

    # Propiedades
    imagen = property(_obtener_imagen, _definir_imagen,
                      doc="Define la imagen a mostrar.")

    def definir_centro(self, (x, y)):
        """ Define en que posición estará el centro del Actor.

        Se puede definir la posición mediante unas coordenadas numéricas o
        mediante texto.

        La forma de definirlo mediante coordenadas numéricas seria así:

        >>> mi_actor.definir_centro((10,50))

        La otra forma de definirlo mediante texto sería:

        >>> mi_actor.definir_centro(('centro','derecha'))

        :param x: Coordenadas horizontal en la que se establecerá el centro
                  del Actor.
        :type x: int
        :param y: Coordenadas vertical en la que se establecerá el centro
                  del Actor.
        :type y: int
        """
        self.centro_x = x
        self.centro_y = y

    def _interpretar_y_convertir_posicion(self, posicion, maximo_valor):
        if posicion in IZQUIERDA + ARRIBA:
            return 0
        elif posicion in CENTRO:
            return int(maximo_valor / 2.0)
        elif posicion in DERECHA + ABAJO:
            return maximo_valor
        else:
            raise Exception("El valor '%s' no corresponde a una posicion, \
                            use numeros o valores como 'izquierda', 'arriba' \
                            etc." % (posicion))

    def obtener_centro(self):
        """ Obtiene las coordenadas del centro del Actor. """
        return (self.centro_x, self.centro_y)

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

        Pulsa la tecla **F8** para ver el centro de los actores
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
        self.x = x
        self.y = y

    def obtener_posicion(self):
        """ Obtiene la posición del Actor en el mundo. """
        return (self.x, self.y)

    def obtener_x(self):
        return self._x

    def definir_x(self, x):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'x', x)

    def obtener_centro_x(self):
        return self._centro_x

    def definir_centro_x(self, x):
        if type(x) == str:
            if x not in IZQUIERDA + CENTRO + DERECHA:
                raise Exception("No puedes definir '%s' como eje horizontal."
                                % (x))
            x = self._interpretar_y_convertir_posicion(x, self.obtener_ancho())
        self.pilas.utils.interpretar_propiedad_numerica(self, 'centro_x', x)

    def obtener_centro_y(self):
        return self._centro_y

    def definir_centro_y(self, y):
        if type(y) == str:
            if y not in ARRIBA + CENTRO + ABAJO:
                raise Exception("No puedes definir '%s' como eje vertical."
                                % (y))
            y = self._interpretar_y_convertir_posicion(y, self.obtener_alto())
        self.pilas.utils.interpretar_propiedad_numerica(self, 'centro_y', y)

    def obtener_z(self):
        return self._z

    def definir_z(self, z):
        self._z = z
        self.pilas.escena_actual()._actores.sort()

    def definir_y(self, y):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'y', y)

    def obtener_y(self):
        return self._y

    def definir_escala(self, s):
        if s < 0.001:
            s = 0.001

        self.escala_x = s
        self.escala_y = s

    def definir_escala_x(self, s):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'escala_x', s)
        if self._escala_x < 0.001:
            self._escala_x = 0.001

    def definir_escala_y(self, s):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'escala_y', s)
        if self._escala_y < 0.001:
            self._escala_y = 0.001

    def obtener_escala(self):
        return self._escala_x

    def obtener_escala_x(self):
        return self._escala_x

    def obtener_escala_y(self):
        return self._escala_y

    def obtener_rotacion(self):
        return self._rotacion

    def definir_rotacion(self, rotacion):
        if isinstance(rotacion, int) or isinstance(rotacion, float):
            rotacion %= 360
        self.pilas.utils.interpretar_propiedad_numerica(self, 'rotacion',
                                                        rotacion)

    def obtener_espejado(self):
        return self._espejado

    def definir_espejado(self, espejado):
        self._espejado = espejado

    def definir_transparencia(self, transparencia):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'transparencia',
                                                        transparencia)

    def obtener_transparencia(self):
        return self._transparencia

    def obtener_fijo(self):
        return self._fijo

    def definir_fijo(self, fijo):
        self._fijo = fijo
        # self.pilas.obtener_escena_actual().cambia_estado_fijo(self)

    def obtener_vx(self):
        return self._vx

    def definir_vy(self):
        return self._vy

    espejado = property(obtener_espejado, definir_espejado,
                        doc="Indica si se tiene que invertir horizontalmente \
                        la imagen del actor.")
    z = property(obtener_z, definir_z,
                 doc="Define lejania respecto del observador.")
    x = property(obtener_x, definir_x, doc="Define la posición horizontal.")
    y = property(obtener_y, definir_y, doc="Define la posición vertical.")
    centro_x = property(obtener_centro_x, definir_centro_x)
    centro_y = property(obtener_centro_y, definir_centro_y)
    vx = property(obtener_vx, None,
                  doc="Obtiene la velocidad horizontal del actor.")
    vy = property(definir_vy, None,
                  doc="Obtiene la velocidad vertical del actor.")
    rotacion = property(obtener_rotacion, definir_rotacion,
                        doc="Angulo de rotación (en grados, de 0 a 360)")
    escala = property(obtener_escala, definir_escala,
                      doc="Escala de tamaño, 1 es normal, \
                      2 al doble de tamaño etc...)")
    escala_x = property(obtener_escala_x, definir_escala_x,
                        doc="Escala de tamaño horizontal, 1 es normal, \
                        2 al doble de tamaño etc...)")
    escala_y = property(obtener_escala_y, definir_escala_y,
                        doc="Escala de tamaño vertical, 1 es normal, 2 al \
                        doble de tamaño etc...)")
    transparencia = property(obtener_transparencia, definir_transparencia,
                             doc="Define el nivel de transparencia, 0 indica \
                             opaco y 100 la maxima transparencia.")
    fijo = property(obtener_fijo, definir_fijo,
                    doc="Indica si el actor debe ser \
                    independiente a la cámara.")

    def eliminar(self):
        """Elimina el actor de la lista que se imprimen en pantalla."""
        self._vivo = False

    def quitar_de_la_escena_completamente(self):
        self._eliminar_anexados()

        try:
            self._eliminar_figura_de_colision()
        except:
            pass

        if self._destruir:
            self._destruir()

    def _eliminar_figura_de_colision(self):
        if self.figura_de_colision:
            self.figura_de_colision.eliminar()

    def _destruir(self):
        """Elimina a un actor pero de manera inmediata."""
        self._vivo = False
        self.eliminar_habilidades()
        self.eliminar_comportamientos()
        # Solo permite eliminar el actor si está en su escena.
        self._eliminar_de_todos_los_grupos_al_que_pertenece()
        self._inhabilitar_actor_completamente()

    def _inhabilitar_actor_completamente(self):
        self.nombre_de_clase = self.__class__.__name__
        self.identificador = id(self)
        # self.__class__ = ActorEliminado

    def esta_eliminado(self):
        return False

    def _eliminar_de_todos_los_grupos_al_que_pertenece(self):
        for g in reversed(self._grupos_a_los_que_pertenece):
            g.eliminar(self)

    def pre_actualizar(self):
        """Actualiza comportamiento y habilidades antes de la actualización.
        También actualiza la velocidad horizontal y vertical que lleva el actor.
        """
        self.actualizar_comportamientos()
        self.actualizar_habilidades()
        self.__actualizar_velocidad()

    def pos_actualizar(self):
        self.mover_figura_de_colision()

    def mover_figura_de_colision(self):
        if getattr(self, 'figura_de_colision', False):
            self.figura_de_colision.x = self.x - self._figura_de_colision_dx
            self.figura_de_colision.y = self.y - self._figura_de_colision_dy
            self.figura_de_colision.rotacion = self.rotacion

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
            raise Exception("No puedes asignar una funcion que espera 2 \
                            o mas argumentos")
        elif cantidad_de_argumentos == 1:
            # Si la función espera un argumento, se re-define la función para
            # que siempre reciba al actor sobre el que se produjo el evento.

            def inyectar_self(f):
                def invocar():
                    f(self)
                return invocar

            callback = inyectar_self(callback)

        grupo_de_callbacks.add(callback)

    def _ejecutar_callback(self, evento, listado_de_callbacks):
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
                        raise ValueError("La funcion no está agregada en \
                                         el callback")

    def set_cuando_hace_click(self, callback):
        if (callback is None):
            self._callback_cuando_hace_click.clear()
        else:
            self.pilas.eventos.click_de_mouse.conectar(self._cuando_hace_click)
            self._agregar_callback(self._callback_cuando_hace_click, callback)

    def get_cuando_hace_click(self):
        return self._callback_cuando_hace_click

    def _cuando_hace_click(self, evento):
        self._ejecutar_callback(evento, self._callback_cuando_hace_click)

    cuando_hace_click = property(get_cuando_hace_click, set_cuando_hace_click)

    def set_cuando_mueve_el_mouse(self, callback):
        if (callback is None):
            self._callback_cuando_mueve_mouse.clear()
        else:
            self.pilas.eventos.mueve_mouse.conectar(self._cuando_mueve_mouse)
            self._agregar_callback(self._callback_cuando_mueve_mouse, callback)

    def get_cuando_mueve_el_mouse(self):
        return self._callback_cuando_mueve_mouse

    def _cuando_mueve_mouse(self, evento):
        self._ejecutar_callback(evento, self._callback_cuando_mueve_mouse)

    cuando_mueve_el_mouse = property(get_cuando_mueve_el_mouse,
                                     set_cuando_mueve_el_mouse, doc="")

    def click_de_mouse(self, callback):
        """Acceso directo para conectar el actor al evento de click_de_mouse.
        No se debe redefinir este método."""
        self.pilas.eventos.click_de_mouse.conectar(callback)

    def mueve_mouse(self, callback):
        """Acceso directo para conectar el actor al evento de mueve_mouse.
        No se debe redefinir este método."""
        self.pilas.eventos.mueve_mouse.conectar(callback)

    def mueve_camara(self, callback):
        """Acceso directo para conectar el actor al evento de mueve_camara.
        No se debe redefinir este método."""
        self.pilas.eventos.mueve_camara.conectar(callback)

    def termina_click(self, callback):
        """Acceso directo para conectar el actor al evento de termina_click.
        No se debe redefinir este método."""
        self.pilas.eventos.termina_click.conectar(callback)

    def mueve_rueda(self, callback):
        """Acceso directo para conectar el actor al evento de mueve_rueda.
        No se debe redefinir este método."""
        self.pilas.eventos.mueve_rueda.conectar(callback)

    def pulsa_tecla(self, callback):
        """Acceso directo para conectar el actor al evento de pulsa_tecla.
        No se debe redefinir este método."""
        self.pilas.eventos.pulsa_tecla.conectar(callback)

    def suelta_tecla(self, callback):
        """Acceso directo para conectar el actor al evento de suelta_tecla.
        No se debe redefinir este método."""
        self.pilas.eventos.suelta_tecla.conectar(callback)

    def pulsa_tecla_escape(self, callback):
        """Acceso directo para conectar el actor al evento de
        pulsa_tecla_escape.
        No se debe redefinir este método."""
        self.pilas.eventos.pulsa_tecla_escape.conectar(callback)

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
        return self.x - (self.centro_x * self.escala)

    def set_izquierda(self, valor):
        def adaptar_valor(x):
            return x + (self.centro_x * self.escala)

        self._aplicar_interpolacion('x', adaptar_valor, valor)


    def _aplicar_interpolacion(self, atributo, adaptar_valor, valor):
        if isinstance(valor, tuple):
            duracion = valor[1]
            valor = [adaptar_valor(x) for x in valor[0]]
            setattr(self, atributo, (valor, duracion))
        elif isinstance(valor, list):
            valor = [adaptar_valor(x) for x in valor]
            setattr(self, atributo, valor)
        elif isinstance(valor, float) or isinstance(valor, int):
            setattr(self, atributo, adaptar_valor(valor))

    izquierda = property(get_izquierda, set_izquierda, doc="Establece el " \
                         "espacio entre la izquierda del actor y el centro " \
                         "de coordenadas del mundo.")

    def get_derecha(self):
        return self.izquierda + self.obtener_ancho() * self.escala

    def set_derecha(self, valor):
        def adaptar_valor(x):
            return x - (self.centro_x * self.escala)

        self._aplicar_interpolacion('x', adaptar_valor, valor)

    derecha = property(get_derecha, set_derecha, doc="Establece el " \
                         "espacio entre la derecha del actor y el centro " \
                         "de coordenadas del mundo.")

    def get_abajo(self):
        return self.get_arriba() - self.alto * self.escala

    def set_abajo(self, valor):
        def adaptar_valor(y):
            return y + (self.centro[1] * self.escala)

        self._aplicar_interpolacion('y', adaptar_valor, valor)

    abajo = property(get_abajo, set_abajo, doc="Establece el " \
                         "espacio entre la parte inferior del actor y el " \
                         "centro de coordenadas del mundo.")

    def get_arriba(self):
        return self.y + (self.centro[1] * self.escala)

    def set_arriba(self, valor):
        def adaptar_valor(y):
            return y - (self.centro[1] * self.escala)

        self._aplicar_interpolacion('y', adaptar_valor, valor)

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
            x = x - self.pilas.escena_actual().camara.x
            y = y - self.pilas.escena_actual().camara.y
        return (self.izquierda <= x <= self.derecha and
                self.abajo <= y <= self.arriba)

    def distancia_con(self, otro_actor):
        """Determina la distancia con el ``otro_actor``

        :param otro_actor: El otro actor para ver la distancia
        :type otro_actor: pilas.actores.Actor

        """
        return self.pilas.utils.distancia_entre_dos_actores(self, otro_actor)

    def actor_mas_cercano(self):
        """Retorna otro actor mas cercano a este actor"""
        return self.pilas.utils.actor_mas_cercano_al_actor(self)

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
        return self.pilas.utils.distancia_entre_dos_puntos((self.x, self.y),
                                                           (x, y))

    def colisiona_con(self, otro_actor):
        """Determina si este actor colisiona con ``otro_actor``

        :param otro_actor: El otro actor para verificar si colisiona.
        :type otro_actor: pilas.actores.Actor

        """
        return self.pilas.utils.colisionan(self, otro_actor)

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
        duplicado = self.__class__(self.pilas)

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

        grupo = self.pilas.actores.fabricar(self.__class__, cantidad - 1)
        grupo.agregar(self)
        return grupo

    def __repr__(self):
        return "<%s en (%d, %d)>" % (self.__class__.__name__, self.x, self.y)

    def imitar(self, otro_actor_o_figura, *args, **kwargs):
        """ Hace que un Actor copie la posición y la rotación de otro Actor o
        Figura fisica.

        Por ejemplo:

        >>> circulo_dinamico = pilas.fisica.Circulo(10, 200, 50)
        >>> mi_actor.imitar(circulo_dinamico)

        :param otro_actor_o_figura: Actor o Figura física a imitar.
        :type otro_actor_o_figura: `Actor`, `Figura`
        """
        self.aprender(self.pilas.habilidades.Imitar, otro_actor_o_figura,
                      *args, **kwargs)

    def decir(self, mensaje, autoeliminar=True):
        """Emite un mensaje usando un globo similar al de los comics.

        :param mensaje: Texto a mostrar en el mensaje.
        :type mensaje: string
        :param autoeliminar: Establece si se eliminará el globo al cabo de
                             unos segundos.
        :type autoeliminar: boolean
        """
        nuevo_actor = self.pilas.actores.Globo(mensaje, self.x, self.y,
                                               autoeliminar=autoeliminar,
                                               objetivo=self)
        nuevo_actor.z = self.z - 1

    def anexar(self, otro_actor):
        """Agrega un Actor a la lista de actores anexados al Actor actual.
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

        (izquierda, derecha, arriba, abajo) = self.pilas.camara.obtener_area_visible()
        return (self.derecha < izquierda or self.izquierda > derecha or
                self.abajo > arriba or self.arriba < abajo)

    def esta_dentro_de_la_pantalla(self):
        return not self.esta_fuera_de_la_pantalla()

    def es_fondo(self):
        """Comprueba si el actor es un fondo del juego."""
        return False

    def obtener_radio_de_colision(self):
        return self._radio_de_colision

    def definir_radio_de_colision(self, radio):
        self._radio_de_colision = radio

        if radio:
            self.crear_figura_de_colision_circular(radio)
        else:
            self.figura_de_colision = None

    radio_de_colision = property(obtener_radio_de_colision, definir_radio_de_colision)

    def definir_area_colision(self, x, y, ancho, alto):
        self.crear_figura_de_colision_rectangular(x, y, ancho, alto)

    def obtener_area_colision(self):
        if getattr(self, 'figura_de_colision'):
            return self.figura_de_colision

        return None


    area_de_colision = property(obtener_area_colision, definir_area_colision)

    def crear_figura_de_colision_circular(self, radio, x=0, y=0):
        self.ff = self.pilas.fisica.Circulo(None, None, radio, dinamica=False, sensor=True)
        self.figura_de_colision = self.ff
        self._figura_de_colision_dx = x
        self._figura_de_colision_dy = y
        #self.mover_figura_de_colision()

    def crear_figura_de_colision_rectangular(self, x, y, ancho, alto):
        self.ff = self.pilas.fisica.Rectangulo(0, 0, ancho, alto, dinamica=False, sensor=True)
        self.figura_de_colision = self.ff
        self._figura_de_colision_dx = x
        self._figura_de_colision_dy = y
        #self.mover_figura_de_colision()

    def disparar(self):
        """Permite que cualquier actor que tenga una habilidad
        para disparar pueda hacerlo."""
        for x in self._habilidades:
            if x.__class__.__name__ == 'Disparar':
                x.disparar()
