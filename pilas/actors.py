# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

from PySFML import sf

all = []

def insert_as_new_actor(actor):
    all.append(actor)

class Actor(sf.Sprite):

    def __init__(self, image_path):
        image = pilas.image.load(image_path)

        sf.Sprite.__init__(self, image)
        insert_as_new_actor(self)
