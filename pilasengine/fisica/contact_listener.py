# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

try:
    import Box2D as box2d
    contact_listener = box2d.b2ContactListener
    __enabled__ = True
except ImportError:
    __enabled__ = False
    class Tmp:
        pass
    contact_listener = Tmp


class ObjetosContactListener(contact_listener):
    """Gestiona las colisiones de los objetos para ejecutar funcionés."""

    def __init__(self, pilas):
        box2d.b2ContactListener.__init__(self)
        self.pilas = pilas

    def BeginContact(self, *args, **kwargs):
        objeto_colisionado_1 = args[0].fixtureA
        objeto_colisionado_2 = args[0].fixtureB

        # Informar la colisión si entran en contacto:
        if objeto_colisionado_1.userData and objeto_colisionado_2.userData:
            print "Colisionan", objeto_colisionado_1.userData['figura'].actor_que_representa_como_area_de_colision, "vs", objeto_colisionado_2.userData['figura'].actor_que_representa_como_area_de_colision


            # TODO: implementar cuando exista el componente colisiones
            pass
            #self.pilas.escena_actual().colisiones.verificar_colisiones_fisicas(objeto_colisionado_1.userData['id'],
            #                                                              objeto_colisionado_2.userData['id'])

