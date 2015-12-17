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

        self.agregar_colision(fixture_1, fixture_2)
        
    def agregar_colision(self, fixture_1, fixture_2):
        actor_asociado_1 = fixture_1.userData.get('actor', None)
        actor_asociado_2 = fixture_2.userData.get('actor', None)

        figura_1 = fixture_1.userData.get('figura', None)
        figura_2 = fixture_2.userData.get('figura', None)
        
        if figura_1 and figura_2 and figura_1 != figura_2:
            figura_1.figuras_en_contacto.append(figura_2)
            figura_2.figuras_en_contacto.append(figura_1)

        #if actor_asociado_1 and actor_asociado_2:
        #    info_colision = {'actor1': actor_asociado_1,
        #                     'actor2': actor_asociado_2}
        #    self._colisiones_en_curso.append(info_colision)

    def eliminar_colision(self, fixture_1, fixture_2):
        actor_asociado_1 = fixture_1.userData.get('actor', None)
        actor_asociado_2 = fixture_2.userData.get('actor', None)

        figura_1 = fixture_1.userData.get('figura', None)
        figura_2 = fixture_2.userData.get('figura', None)
        
        if figura_1 and figura_2 and figura_1 != figura_2:
            if figura_2 in figura_1.figuras_en_contacto:
                figura_1.figuras_en_contacto.remove(figura_2)

            if figura_1 in figura_2.figuras_en_contacto:
                figura_2.figuras_en_contacto.remove(figura_1)

        #if actor_asociado_1 and actor_asociado_2:
        #    info_colision = {'actor1': actor_asociado_1,
        #                     'actor2': actor_asociado_2}
        #    self._colisiones_en_curso.append(info_colision)

    def EndContact(self, *args, **kwargs):
        # TODO: informar el fin de la colisión.
        fixture_1 = args[0].fixtureA
        fixture_2 = args[0].fixtureB
        self.detener_figuras_estaticas(args[0])
        self.eliminar_colision(fixture_1, fixture_2)


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
