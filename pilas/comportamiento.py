# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class Comportamiento:
    "Representa un comportamiento (estrategia) que se puede anexar a un actor."

    def __init__(self, receptor):
        self.receptor = receptor

    def actualizar(self):
        pass
