# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
import pilas.actores
from pilas.escena import Base
import pilas.colores
import pilas.fondos


class Normal(Base):
    """ Escena básica de pilas.
    Si no se define ninguna escena, cuando se ejecuta:

    >>> pilas.iniciar()
    >>> pilas.ejecutar()

    esta es la escena que se muestra en la pantalla.
    """

    def __init__(self):
        Base.__init__(self)

    def iniciar(self):
        self.fondo = pilas.fondos.Plano()

    def set_fondo(self, unFondo):
		self.fondo = unFondo
    
    def get_fondo(self):
		return self.fondo
		
class Aviso(Base):
    """ Escena básica de pilas.
    Si no se define ninguna escena, cuando se ejecuta:

    >>> pilas.iniciar()
    >>> pilas.ejecutar()

    esta es la escena que se muestra en la pantalla.
    """

    def __init__(self):
        Base.__init__(self)

    def iniciar(self):
        fondo = pilas.fondos.Color(pilas.colores.grisclaro)
        fondo.id = "aviso1"
        texto = pilas.actores.Texto("Estas ejecutando la nueva version de Pilas.\n\nDebes actualizar tu codigo para que funcione\ncorrectamente.\n\nTe recomendamos que visites la documentacion.\nhttp://pilas.readthedocs.org/en/latest/\n\n\
        Disculpa las molestias.")
        texto.y = 300
        texto.id = "aviso2"
        self.pulsa_tecla_escape.conectar(self.salir)

    def salir(self, evento):
        pilas.terminar()

    def actualizar(self):
        if len(self.actores) > 1:
            for actor in self.actores:
                if not('aviso' in actor.id):
                    actor.destruir()
