# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor


class Boton(Actor):
    """Representa un boton que reacciona al ser presionado.

    .. image:: ../../pilas/data/manual/imagenes/actores/boton_normal.png

    """

    def __init__(self, pilas, x=0, y=0,
                 ruta_normal='boton/boton_normal.png',
                 ruta_press='boton/boton_press.png',
                 ruta_over='boton/boton_over.png'):

        super(Boton, self).__init__(pilas, x=x, y=y)
        self.imagen_normal = self.pilas.imagenes.cargar(ruta_normal)
        self.imagen_press = self.pilas.imagenes.cargar(ruta_press)
        self.imagen_over = self.pilas.imagenes.cargar(ruta_over)

        self.funciones_normal = []
        self.funciones_press = []
        self.funciones_over = []

        self.estado = True
        self.imagen = self.imagen_normal

        self.pilas.eventos.mueve_mouse.conectar(self.detection_move_mouse)
        self.pilas.eventos.click_de_mouse.conectar(self.detection_click_mouse)
        self.pilas.eventos.termina_click.conectar(self.detection_end_click_mouse)

    #funciones que conectan evento(press, over, normal) a funciones
    def conectar_normal(self, funcion, *args, **kwargs):
        """ Permite conectar un metodo para que sea ejecutado cuando el botón
        pase al estado normal.

        >>> def cuando_deja_de_pulsar():
        >>>     b.pintar_normal()
        >>>
        >>> mi_boton.conectar_normal(cuando_deja_de_pulsar)

        :param funcion: Método a llamar cuando el botón pase a estado Normal.
        :param arg: Argumentos a pasar a la funcion.
        """
        t = (funcion, args, kwargs)
        self.funciones_normal.append(t)

    def conectar_presionado(self, funcion, *args, **kwargs):
        """ Permite conectar un metodo para que sea ejecutado cuando el botón
        se presiona.

        >>> def cuando_pulsan_el_boton():
        >>>     b.pintar_presionado()
        >>>
        >>> mi_boton.conectar_presionado(cuando_pulsan_el_boton)

        :param funcion: Método a llamar cuando el botón pase a estado Normal.
        :param arg: Argumentos a pasar a la funcion.
        """
        t = (funcion, args, kwargs)
        self.funciones_press.append(t)

    def conectar_sobre(self, funcion, *args, **kwargs):
        """ Permite conectar un metodo para que sea ejecutado cuando el ratón
        pasa por encima del botón.

        >>> def cuando_pasa_sobre_el_boton():
        >>>     b.pintar_sobre()
        >>>
        >>> mi_boton.conectar_sobre(cuando_pasa_sobre_el_boton)

        :param funcion: Método a llamar cuando el botón pase a estado Normal.
        :param arg: Argumentos a pasar a la funcion.
        """
        t = (funcion, args, kwargs)
        self.funciones_over.append(t)

    def desconectar_normal_todo(self):
        """ Elimina todas las funciones asociadas al estado normal del botón. """
        self.funciones_normal = []

    def desconectar_presionado_todo(self):
        """ Elimina todas las funciones asociadas al estado presionado del botón. """
        self.funciones_press = []

    def desconectar_sobre_todo(self):
        """ Elimina todas las funciones asociadas al estado sobre del botón. """
        self.funciones_over = []

    def desconectar_normal(self, funcion, *args, **kwargs):
        """ Elimina el método indicado asociado al estado normal del botón.

        :param funcion: Método al que se llama cuando el botón pasa estado Normal.
        :param arg: Argumentos que se pasaban a la funcion.
        """
        t = (funcion, args, kwargs)
        self.funciones_normal.remove(t)

    def desconectar_presionado(self, funcion, *args, **kwargs):
        """ Elimina el método indicado asociado al estado presinado del botón.

        :param funcion: Método al que se llama cuando el botón pasa estado Presionado.
        :param arg: Argumentos que se pasaban a la funcion.
        """
        t = (funcion, args, kwargs)
        self.funciones_press.remove(t)

    def desconectar_sobre(self, funcion, *args, **kwargs):
        """ Elimina el método indicado asociado al estado sobre del botón.

        :param funcion: Método al que se llama cuando el botón pasa estado Sobre.
        :param arg: Argumentos que se pasaban a la funcion.
        """
        t = (funcion, args, kwargs)
        self.funciones_over.remove(t)

    def ejecutar_funciones_normal(self):
        if self.estado:
            for funcion, args, kwargs in self.funciones_normal:
                funcion(*args, **kwargs)

    def ejecutar_funciones_press(self):
        if self.estado:
            for funcion, args, kwargs in self.funciones_press:
                funcion(*args, **kwargs)

    def ejecutar_funciones_over(self):
        if self.estado:
            for funcion, args, kwargs in self.funciones_over:
                funcion(*args, **kwargs)

    # funciones para inactivar o activar las funciones conectadas
    def activar(self):
        self.estado = True

    def desactivar(self):
        self.estado = False

    # funciones que cambian la imagen del boton
    def pintar_normal(self):
        """ Dibuja el botón en estado normal. """
        self.imagen = self.imagen_normal

    def pintar_presionado(self, ruta_press=None):
        """ Dibuja el botón en estado presinado.

        :param ruta_press: Opcional. Ruta de la imagen del boton presionado.
        :type ruta_press: string
        """
        if not ruta_press:
            ruta_press = self.imagen_press

        self.imagen = ruta_press

    def pintar_sobre(self):
        """ Dibuja el botón en estado sobre. """
        self.imagen = self.imagen_over

    def detection_move_mouse(self, evento):
        if self.colisiona_con_un_punto(evento.x, evento.y):
            self.ejecutar_funciones_over()
        else:
            self.ejecutar_funciones_normal()

    def detection_click_mouse(self, click):
        if self.colisiona_con_un_punto(click.x, click.y):
            self.ejecutar_funciones_press()

    def detection_end_click_mouse(self, end_click):
        pass
