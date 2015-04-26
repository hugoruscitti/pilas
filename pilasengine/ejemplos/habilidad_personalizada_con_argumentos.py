import pilasengine

class GirarPorSiempre(pilasengine.habilidades.Habilidad):

    def iniciar(self, receptor, velocidad=1):
        self.receptor = receptor
        self.velocidad = velocidad

    def actualizar(self):
        self.receptor.rotacion += self.velocidad

pilas = pilasengine.iniciar()

a = pilas.actores.Mono()
pilas.habilidades.vincular(GirarPorSiempre)
a.aprender('GirarPorSiempre', 2)
pilas.avisar("Girando por siempre...")
pilas.ejecutar()
