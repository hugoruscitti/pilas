# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


import math
import inspect

import pilas
import utils
from actor import Actor

todos = []

__doc__ = """
Módulo pilas.actores
====================

El módulo actores contiene una serie de clases
para representar personajes de videojuegos.

Para crear actores en una escena del juego simplemente
se tiene que crear un nuevo objeto a partir de una
clase.

Por ejemplo, para crear un pongüino podríamos
escribir la siguiente sentencia:

    >>> p = pilas.actores.Pingu()

"""



from mono import Mono
from ejes import Ejes
from animado import Animado
from animacion import Animacion
from explosion import Explosion
from bomba import Bomba
from pingu import Pingu
from banana import Banana
from texto import Texto
from temporizador import Temporizador
from moneda import Moneda
from pizarra import Pizarra
from pelota import Pelota
from puntaje import Puntaje
from estrella import Estrella
from caja import Caja
from nave import Nave
from navekids import NaveKids
from cursordisparo import CursorDisparo
from piedra import Piedra
from menu import Menu
from opcion import Opcion
from tortuga import Tortuga
from mapa import Mapa
from mapatiled import MapaTiled
from martian import Martian
from boton import Boton
from aceituna import Aceituna
from globo import Globo
from dialogo import Dialogo
from globoelegir import GloboElegir
from pausa import Pausa
from mano import CursorMano
from cooperativista import Cooperativista
from zanahoria import Zanahoria
from energia import Energia
from texto_inferior import TextoInferior
from sonido import Sonido
from personajes_rpg import Calvo
from personajes_rpg import Maton
from pacman import Pacman
from fantasma import Fantasma
from humo import Humo
from proyectil import Bala
from proyectil import Misil
from proyectil import Dinamita
from proyectil import EstrellaNinja
from torreta import Torreta
from ovni import Ovni


def listar_actores():
    """Devuelve una lista con todos los actores disponibles para crear en pilas

    """
    return [k for k, v in vars(pilas.actores).items()
             if inspect.isclass(v) and issubclass(v, Actor)]

