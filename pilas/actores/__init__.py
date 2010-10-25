# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

from PySFML import sf
import math

todos = []

Actor = pilas.motor.Actor

print "Cargando modulo actores, usando el motor '%s'" %(pilas.motor.__class__.__name__)




from mono import *
from tortuga import *
from texto import *
from ejes import *
from pingu import Pingu
from pizarra import Pizarra
from animado import Animado
from animacion import Animacion
from explosion import Explosion
from banana import Banana
from bomba import Bomba
from moneda import Moneda
