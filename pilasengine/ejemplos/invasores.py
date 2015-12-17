# -*- coding: utf-8
import pilasengine

pilas = pilasengine.iniciar()

puntaje = pilas.actores.Puntaje(-280, 200, color=pilas.colores.blanco)


class AceitunaEnemiga(pilasengine.actores.Aceituna):

    def iniciar(self):
        self.imagen = "aceituna.png"
        self.aprender( pilas.habilidades.PuedeExplotarConHumo )
        self.x = pilas.azar(-200, 200)
        self.y = 290
        self.velocidad = pilas.azar(10, 40) / 10.0

    def actualizar(self):
        self.rotacion += 10
        self.y -= self.velocidad

        # Elimina el objeto cuando sale de la pantalla.
        if self.y < -300:
            self.eliminar()

fondo = pilas.fondos.Galaxia(dy=-5)

enemigos = pilas.actores.Grupo()

def crear_enemigo():
    actor = AceitunaEnemiga(pilas)
    enemigos.agregar(actor)

pilas.tareas.siempre(0.5, crear_enemigo)

nave = pilas.actores.NaveRoja(y=-200)
nave.aprender(pilas.habilidades.LimitadoABordesDePantalla)
nave.definir_enemigos(enemigos, puntaje.aumentar)

pilas.colisiones.agregar(nave, enemigos, nave.eliminar)

pilas.avisar(u"Pulsá los direccionales del teclado o espacio para disparar.")
pilas.ejecutar()
