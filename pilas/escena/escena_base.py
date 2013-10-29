# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from pilas import tareas, colisiones, pytweener, camara
from pilas.evento import Evento


class Base(object):
    """ Escena base abstracta de la que deben heredar el resto de escenas.

        >>> class MiEscena(Base):
        >>>
        >>>    def __init__(self):
        >>>        Base.__init__(self)
        >>>
        >>>    def iniciar(self):
        >>>        fondo = pilas.fondos.Color(pilas.colores.grisclaro)

        Si heredas de esta clase DEBES redefinir el método "iniciar".
        Como se muestra en el ejemplo anterior.
    """
    def __init__(self):

        # Identificador de la escena. Sólo util para efectuar algún debug.
        self.id = ""

        # Actores que participan en la escena.
        self.actores = []

        # Camara de la escena.
        self.camara = camara.Camara()

        # Eventos asociados a la escena.
        self.mueve_camara = Evento('mueve_camara')               # ['x', 'y', 'dx', 'dy']
        self.mueve_mouse = Evento('mueve_mouse')                 # ['x', 'y', 'dx', 'dy']
        self.click_de_mouse = Evento('click_de_mouse')           # ['button', 'x', 'y']
        self.termina_click = Evento('termina_click')             # ['button', 'x', 'y']
        self.mueve_rueda = Evento('mueve_rueda')                 # ['delta']
        self.pulsa_tecla = Evento('pulsa_tecla')                 # ['codigo', 'texto']
        self.suelta_tecla = Evento('suelta_tecla')               # ['codigo', 'texto']
        self.pulsa_tecla_escape = Evento('pulsa_tecla_escape')   # []
        self.actualizar = Evento('actualizar')                   # []
        self.log = Evento('log')                                 # ['data']

        self.control = pilas.control.Control(self)

        # Gestor de tareas
        self.tareas = tareas.Tareas()

        # Gestor de colisiones
        self.colisiones = colisiones.Colisiones()

        # Generador de interpolaciones
        self.tweener = pytweener.Tweener()

        # Administrador de la fisica de la escena.
        self.fisica = pilas.mundo.crear_motor_fisica()

        # Control para saber si se ha iniciado la escena y poder actualizarla.
        self.iniciada = False

        # Para resetear la posición de la camara
        self.camara_x = 0
        self.camara_y = 0

        self.escena_pausa = False

    def iniciar(self):
        """ Este método debe ser reimplementado en todas las clases que
        hereden de ella.

        >>>    def iniciar(self):
        >>>        fondo = pilas.fondos.Color(pilas.colores.grisclaro)

        """
        raise Exception("Debes de re-definir el metodo iniciar.")

    def pausar(self):
        """ Este método es llamado por el gestor de escenas cuando se
        ::almacena:: una escena para llamar a otra nueva.

        >>> pilas.almacenar_escena(EscenaDeOpciones())

        Al efectuar esta instrucción el gestor llamará primero a nuestro
        método ::pausar:: antes de cambiar a la escena que le hemos indicado.
        """
        pass

    def reanudar(self):
        """ Este método es llamado por el gestor de escenas cuando se
        ::recupera:: una escena que habia sido almacenada anteriormente.

        >>> pilas.recuperar_escena()

        Al efectuar esta instrucción el gestor llamará primero a nuestro
        método ::reanudar:: antes de cambiar a la escena que habiamos
        almacenado.
        """
        pass

    # Estos metodos no deben ser sobreescritos en las clases que
    # hereden de ella.

    def _pausar_fisica(self):
        self.fisica.pausar_mundo()

    def _reanudar_fisica(self):
        self.fisica.reanudar_mundo()

    def _actualizar_eventos(self):
        self.tweener.update(16)
        self.tareas.actualizar(1 / 60.0)
        self.colisiones.verificar_colisiones()

    def _actualizar_fisica(self):
        if self.fisica:
            self.fisica.actualizar()

    def _limpiar(self):
        for actor in self.actores:
            actor.destruir()

        self.tareas.eliminar_todas()
        self.tweener.eliminar_todas()
        if self.fisica:
            self.fisica.reiniciar()

    def guardar_posicion_camara(self):
        """ Este método se llama cuando se cambia de escena y así poder
        recuperar la ubicación de la cámara en la escena actual
        """
        self.camara_x = self.camara.x
        self.camara_y = self.camara.y

    def recuperar_posicion_camara(self):
        self.camara.x = self.camara_x
        self.camara.y = self.camara_y
