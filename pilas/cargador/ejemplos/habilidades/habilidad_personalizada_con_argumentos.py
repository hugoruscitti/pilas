import pilas

class GirarPorSiempre(pilas.habilidades.Habilidad):
    
    def __init__(self, receptor, velocidad=1):
        self.receptor = receptor
        self.velocidad = velocidad
    
    def actualizar(self):
        self.receptor.rotacion += self.velocidad

pilas.iniciar()

a = pilas.actores.Mono()
a.aprender(GirarPorSiempre, 20)
pilas.avisar("Girando por siempre...")
pilas.ejecutar()
