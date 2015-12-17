import pilasengine

class GirarPorSiempre(pilasengine.habilidades.Habilidad):

    def actualizar(self):
        self.receptor.rotacion += 1

pilas = pilasengine.iniciar()

a = pilas.actores.Mono()
pilas.habilidades.vincular(GirarPorSiempre)
a.aprender('GirarPorSiempre')
pilas.ejecutar()
