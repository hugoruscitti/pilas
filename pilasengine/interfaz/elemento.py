# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine.actores import actor

class Elemento(actor.Actor):

    def __init__(self, pilas=None):
        super(Elemento, self).__init__(pilas)
        self.z = -1000
        self.radio_de_colision = None