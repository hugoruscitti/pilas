# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine import actores


class Boton(actores.Actor):
    """Representa un boton que reacciona al ser presionado.

    .. image:: images/actores/boton_normal.png

    """

    def __init__(self, pilas, x=0, y=0,
                ruta_normal='boton/boton_normal.png',
                ruta_press='boton/boton_press.png',
                ruta_over='boton/boton_over.png',
                ):
        self.ruta_normal = ruta_normal
        self.ruta_press = ruta_press
        self.ruta_over = ruta_over

        self.funciones_normal = []
        self.funciones_press = []
        self.funciones_over = []

        self.estado = True

        actores.Actor.__init__(self, pilas, x=x, y=y)
        self._cargar_imagenes(self.ruta_normal, self.ruta_press, self.ruta_over)
        self.imagen = self.ruta_normal

        self.pilas.escena_actual().mueve_mouse.conectar(self.detection_move_mouse)
        self.pilas.escena_actual().click_de_mouse.conectar(self.detection_click_mouse)
        self.pilas.escena_actual().termina_click.conectar(self.detection_end_click_mouse)

    def _cargar_imagenes(self, ruta_normal, ruta_press, ruta_over):
        self.ruta_normal = ruta_normal
        self.ruta_press = ruta_press
        self.ruta_over = ruta_over

        self.imagen_over = self.pilas.imagenes.cargar(ruta_over)
        self.imagen_normal = self.pilas.imagenes.cargar(ruta_normal)
        self.imagen_press = self.pilas.imagenes.cargar(ruta_press)

    #funciones que conectan evento(press, over, normal) a funciones
    def conectar_normal(self, funcion, arg="null"):
        """ Permite conectar un metodo para que sea ejecutado cuando el botón
        pase al estado normal.

        >>> def cuando_deja_de_pulsar():
        >>>     b.pintar_normal()
        >>>
        >>> mi_boton.conectar_normal(cuando_deja_de_pulsar)

        :param funcion: Método a llamar cuando el botón pase a estado Normal.
        :param arg: Argumentos a pasar a la funcion.
        """
        t = (funcion, arg)
        self.funciones_normal.append(t)

    def conectar_presionado(self, funcion, arg="null"):
        """ Permite conectar un metodo para que sea ejecutado cuando el botón
        se presiona.

        >>> def cuando_pulsan_el_boton():
        >>>     b.pintar_presionado()
        >>>
        >>> mi_boton.conectar_presionado(cuando_pulsan_el_boton)

        :param funcion: Método a llamar cuando el botón pase a estado Normal.
        :param arg: Argumentos a pasar a la funcion.
        """
        t = (funcion, arg)
        self.funciones_press.append(t)

    def conectar_sobre(self, funcion, arg="null"):
        """ Permite conectar un metodo para que sea ejecutado cuando el ratón
        pasa por encima del botón.

        >>> def cuando_pasa_sobre_el_boton():
        >>>     b.pintar_sobre()
        >>>
        >>> mi_boton.conectar_sobre(cuando_pasa_sobre_el_boton)

        :param funcion: Método a llamar cuando el botón pase a estado Normal.
        :param arg: Argumentos a pasar a la funcion.
        """
        t = (funcion, arg)
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

    def desconectar_normal(self, funcion, arg="null"):
        """ Elimina el método indicado asociado al estado normal del botón.

        :param funcion: Método al que se llama cuando el botón pasa estado Normal.
        :param arg: Argumentos que se pasaban a la funcion.
        """
        t = (funcion, arg)
        self.funciones_normal.remove(t)

    def desconectar_presionado(self, funcion, arg="null"):
        """ Elimina el método indicado asociado al estado presinado del botón.

        :param funcion: Método al que se llama cuando el botón pasa estado Presionado.
        :param arg: Argumentos que se pasaban a la funcion.
        """
        t = (funcion, arg)
        self.funciones_press.remove(t)

    def desconectar_sobre(self, funcion, arg="null"):
        """ Elimina el método indicado asociado al estado sobre del botón.

        :param funcion: Método al que se llama cuando el botón pasa estado Sobre.
        :param arg: Argumentos que se pasaban a la funcion.
        """
        t = (funcion, arg)
        self.funciones_over.remove(t)

    def ejecutar_funciones_normal(self):
        if self.estado == True:
            for i in self.funciones_normal:
                if i[1] == "null":
                    i[0]()
                else:
                    i[0](i[1])

    def ejecutar_funciones_press(self):
        if self.estado == True:
            for i in self.funciones_press:
                if i[1] == "null":
                    i[0]()
                else:
                    i[0](i[1])

    def ejecutar_funciones_over(self):
        if self.estado == True:
            for i in self.funciones_over:
                if i[1] == "null":
                    i[0]()
                else:
                    i[0](i[1])

    # funciones para inactivar o activar las funciones conectadas
    def activar(self):
        self.estado = True

    def desactivar(self):
        self.estado = False

    # funciones que cambian la imagen del boton
    def pintar_normal(self):
        """ Dibuja el botón en estado normal. """
        self.definir_imagen(self.imagen_normal)

    def pintar_presionado(self, ruta_press="null"):
        """ Dibuja el botón en estado presinado.

        :param ruta_press: Opcional. Ruta de la imagen del boton presionado.
        :type ruta_press: string
        """
        if ruta_press == "null":
            self.imagen_press = self.pilas.imagenes.cargar(self.ruta_press)
        else:
            self.imagen_press = self.pilas.imagenes.cargar(ruta_press)

        self.definir_imagen(self.imagen_press)

    def pintar_sobre(self):
        """ Dibuja el botón en estado sobre. """
        self.definir_imagen(self.imagen_over)

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