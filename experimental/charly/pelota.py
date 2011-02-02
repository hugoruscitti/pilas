import pilas
from pilas.comportamientos import Comportamiento

class Pelota(pilas.actores.Actor):
    
    def __init__(self, x=0, y=0, escala=1):
        pilas.actores.Actor.__init__(self, "pelota.png", x=x, y=y)
        self.escala = escala
        self.abajo = -235
        self.hacer(Normal())



class Normal(Comportamiento):
    
    def actualizar(self):
        self.receptor.rotacion -= 2
        self.receptor.x -= 2
        
        
class ControladaPorElProtagonista(Comportamiento):
    
    def actualizar(self):
        pass
    
class Empujada(Comportamiento):
    
    def actualizar(self):
        self.receptor.rotacion -= 10
        self.receptor.x -= 10