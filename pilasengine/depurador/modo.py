# -*- encoding: utf-8 -*-

class ModoDepurador(object):
    tecla = "F00"

    def __init__(self, pilas, depurador):
        self.pilas = pilas
        self.depurador = depurador

    def realizar_dibujado(self, painter, lienzo):
        pass

    def dibuja_actor(self, painter, lienzo, actor):
        pass

    def termina_dibujado(self, painter, lienzo):
        pass

    def orden_de_tecla(self):
        return int(self.tecla[1:])

    def sale_del_modo(self):
        pass

    def _obtener_posicion_relativa_a_camara(self, actor):
        if actor.fijo:
            return (actor.x, actor.y)
        else:
            return (actor.x - pilas.escena_actual().camara.x, actor.y - pilas.escena_actual().camara.y)
