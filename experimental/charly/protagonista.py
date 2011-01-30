import pilas
from pilas.actores import Actor
from pilas.comportamientos import Comportamiento

VELOCIDAD = 4

class Protagonista(Actor):
    "Representa una tortuga que se mueve por la pantalla como la tortuga de Logo."

    def __init__(self, pelotas):
        self.pelotas = pelotas
        Actor.__init__(self)
        self.animacion = pilas.imagenes.cargar_grilla("pingu.png", 10)
        self.definir_cuadro(4)
        self.hacer(Saltando(0))
        self.radio_de_colision = 30

    def definir_cuadro(self, indice):
        self.animacion.definir_cuadro(indice)
        self.animacion.asignar(self)


class EnEquilibrio(Comportamiento):

    def __init__(self, pelota_que_pisa):
        self.cuadros = [5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9]
        self.paso = 0
        self.pelota_que_pisa = pelota_que_pisa

    def actualizar(self):

        if pilas.mundo.control.izquierda:
            self.avanzar_animacion()
            self.receptor.x -= VELOCIDAD
            self.pelota_que_pisa.rotacion -= VELOCIDAD
        elif pilas.mundo.control.derecha:
            self.receptor.x += VELOCIDAD
            self.pelota_que_pisa.rotacion += VELOCIDAD
            self.avanzar_animacion()
        else:
            self.receptor.definir_cuadro(4)

        if pilas.mundo.control.arriba:
            self.receptor.hacer(Saltando())

        self.pelota_que_pisa.x = self.receptor.x

    def avanzar_animacion(self):
        self.paso += 1

        if self.paso >= len(self.cuadros):
            self.paso = 0

        self.receptor.definir_cuadro(self.cuadros[self.paso])

class Saltando(Comportamiento):

    def __init__(self, dy=10):
        self.dy = dy
        
    def iniciar(self, receptor):
        self.receptor = receptor
        self.receptor.definir_cuadro(0)
        self.origen = self.receptor.y

    def actualizar(self):
        self.receptor.y += self.dy
        self.dy -= 0.3

        pelota_que_pisa = self.pisa_una_pelota()
        
        if pelota_que_pisa:
            self.receptor.hacer(EnEquilibrio(pelota_que_pisa))

        if pilas.mundo.control.izquierda:
            self.receptor.x -= VELOCIDAD
        elif pilas.mundo.control.derecha:
            self.receptor.x += VELOCIDAD

    def pisa_una_pelota(self):
        for pelota in self.receptor.pelotas:
            actor = self.receptor
            delta = 10
    
            if pelota.arriba - delta < actor.abajo < pelota.arriba + delta:
                if pelota.izquierda < actor.x < pelota.derecha:
                    actor.abajo = pelota.arriba
                    pelota.x = actor.x
                    return pelota
