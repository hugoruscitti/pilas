import camara
from pilasengine.actores import grupo
from pilasengine.utils import pitweener

class Escena(object):

    def __init__(self, pilas):
        self.pilas = pilas
        pilas.log("Creando una escena: ", self)
        self.camara = camara.Camara(pilas, self)
        self.tweener = pitweener.Tweener()
        self._actores = grupo.Grupo(pilas)
        self.grupos = []

    def iniciar(self):
        pass

    def actualizar(self):
        pass

    def terminar(self):
        pass

    def actualizar_interpolaciones(self):
        self.tweener.update()

    def actualizar_actores(self):
        for x in self._actores.obtener_actores():
            x.actualizar()

    def dibujar_actores(self, painter):
        painter.save()

        self.camara.aplicar_transformaciones_completas(painter)

        for x in self._actores.obtener_actores(fijos=False, sin_padre=True):
            x.dibujar(painter)

        painter.restore()

        painter.save()
        self.camara.aplicar_translacion(painter)

        for x in self._actores.obtener_actores(fijos=True, sin_padre=True):
            x.dibujar(painter)

        painter.restore()

    def agregar_actor(self, actor):
        self._actores.agregar(actor)

    def agregar_grupo(self, grupo):
        self.grupos.append(grupo)