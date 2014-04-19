import camara

class Escena(object):

    def __init__(self, pilas):
        self.pilas = pilas
        pilas.log("Creando una escena: ", self)
        self.camara = camara.Camara(pilas, self)
        self.actores = []

    def iniciar(self):
        pass

    def actualizar(self):
        pass

    def terminar(self):
        pass

    def actualizar_actores(self):
        for x in self.actores:
            x.actualizar()

    def dibujar_actores(self, painter):
        painter.save()
        self.camara.aplicar_transformaciones(painter)

        for x in self.actores:
            x.dibujar(painter)

        painter.restore()

    def agregar_actor(self, actor):
        self.actores.append(actor)