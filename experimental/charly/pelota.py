import pilas


class Pelota(pilas.actores.Actor):
    
    def __init__(self, x=0, y=0, escala=1):
        pilas.actores.Actor.__init__(self, "pelota.png", x=x, y=y)
        self.escala = escala
        self.abajo = -235
        
