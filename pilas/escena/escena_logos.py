# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
from collections import OrderedDict

import pilas.actores
from pilas.escena import Base
from pilas.escena import Normal
import pilas.sonidos
import pilas.fondos
import pilas.imagenes
import pilas.mundo


class Logos(Normal):
    """Esta escena es el clásico inicio donde se van mostrando todas las
    tecnologías y empresas involucradas en el juego y luego pasa a la primer
    escena propiamente del juego.

    Por defecto ya agrega como primer pantalla el logo de Pilas en 640*480.

    Por ejemplo, para mostrar el logo de pilas seguido del tuyo y
    luego pasar a la escena de *Menú Principal* podrias hacer:

        >>> logos = pilas.escenas.Logos(MiMenuPrincipal())
        >>> logos.agregar_logo("mi_logo.png")
        >>> pilas.cambiar_escena(logos)

    Si por otro lado si querés que el logo se muestre en pantalla por 10
    segundos, y no 2 como es por defecto, puedes hacer:

        >>> logos = pilas.escenas.Logos(MiMenuPrincipal())
        >>> logos.agregar_logo("mi_logo.png", timer=10)
        >>> pilas.cambiar_escena(logos)

    También puedes agregarle alguna musica o sonido a tus logos utilizando el
    parámetro ``sonido`` en agregar logo.

        >>> logos = pilas.escenas.Logos(MiMenuPrincipal())
        >>> logos.agregar_logo("mi_logo.png", sonido="misonido.mp3")
        >>> pilas.cambiar_escena(logos)

    """

    def __init__(self, escena_siguiente, pilas_logo=True):
        """Constructor de Logos

        :param escena_siguiente: Cual sera la escena siguiente a mostrar luego
                                 de todos los logos.
        :type escena_siguiente: pilas.escena.Base
        :param pilas_logo: Si el primer logo a mostrar va a ser el de Pilas
        :type pilas_logo: bool

        """
        super(Logos, self).__init__()
        self.escena_siguiente = escena_siguiente
        self._logos_futuros = OrderedDict()
        self._sonido = None
        if pilas_logo:
            self.agregar_logo("pilasengine.png")

    def agregar_logo(self, imagen, timer=2.5, sonido=None):
        """Agrega una nueva imagen a la lista de imagenes a mostrar antes
        de pasar a la escena siguiente

        :param imagen: El nombre de una imagen a mostrar.
        :type imagen: str
        :param timer: Cuanto tiempo quieres que se muestre esta imagen.
        :type timer: float
        :param sonido: El sonido para la imagen
        :type sonido: str

        """
        self._logos_futuros[imagen] = (timer, sonido)

    def iniciar(self):
        # tomamos el primer logo
        imagen, data = self._logos_futuros.popitem(False)
        timer, sonido = data
        pilas.fondos.Fondo(imagen=pilas.imagenes.cargar_imagen(imagen))
        if sonido:
            self._sonido = pilas.sonidos.cargar(sonido)
            self._sonido.reproducir()
        pilas.mundo.agregar_tarea(timer, self._siguiente)
        self.pulsa_tecla.conectar(self._siguiente)
        self.click_de_mouse.conectar(self._siguiente)

    def _siguiente(self, *args, **kwargs):
        if self._sonido:
            self._sonido.detener()
        if self._logos_futuros:
            siguiente_logos = Logos(self.escena_siguiente, pilas_logo=False)
            siguiente_logos._logos_futuros = self._logos_futuros
            pilas.cambiar_escena(siguiente_logos)
        else:
            pilas.cambiar_escena(self.escena_siguiente)
