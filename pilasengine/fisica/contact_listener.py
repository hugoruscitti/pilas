# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import Box2D as box2d

class ObjetosContactListener(box2d.b2ContactListener):
    """Gestiona las colisiones de los objetos para ejecutar funcionés."""

    def __init__(self, pilas):
        box2d.b2ContactListener.__init__(self)
        self.pilas = pilas

    def BeginContact(self, *args, **kwargs):
        fixture_1 = args[0].fixtureA
        fixture_2 = args[0].fixtureB

        # Informar la colisión si entran en contacto:
        #if fixture_1.userData and fixture_2.userData:
        #    self.pilas.colisiones.notificar_colision(fixture_1, fixture_2)

        print "Comienza colision entre ", id(fixture_1), id(fixture_2)

    def EndContact(self, *args, **kwargs):
        fixture_1 = args[0].fixtureA
        fixture_2 = args[0].fixtureB

        print "fin de colision entre ", id(fixture_1), id(fixture_2)

    def PreSolve(self, contact, old):
        fixture_1 = contact.fixtureA
        fixture_2 = contact.fixtureB

        if fixture_1.userData['sensor'] or fixture_2.userData['sensor']:
            contact.enabled = False
            print "Ignorando contact", fixture_1, fixture_2
        #print contact, old
        pass