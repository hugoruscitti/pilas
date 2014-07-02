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

        self.detener_figuras_estaticas(args[0])
        self.pilas.colisiones.notificar_colision(fixture_1, fixture_2)

    def EndContact(self, *args, **kwargs):
        # TODO: informar el fin de la colisión.
        self.detener_figuras_estaticas(args[0])

    def PreSolve(self, contact, old):
        fixture_1 = contact.fixtureA
        fixture_2 = contact.fixtureB
        self.detener_figuras_estaticas(contact)

        # Hace que las figuras marcadas como sensores no generen
        # una respuesta de colisión física (solamente programada).
        if fixture_1.userData['sensor'] or fixture_2.userData['sensor']:
            contact.enabled = False

    def PostSolve(self, contact, old):
        self.detener_figuras_estaticas(contact)

    def detener_figuras_estaticas(self, contact):
        fixture_1 = contact.fixtureA
        fixture_2 = contact.fixtureB

        def detener(body):
            body.linearVelocity = (0, 0)
            body.angularVelocity = 0

        if not fixture_1.userData['dinamica']:
            detener(fixture_1.body)

        if not fixture_2.userData['dinamica']:
            detener(fixture_2.body)