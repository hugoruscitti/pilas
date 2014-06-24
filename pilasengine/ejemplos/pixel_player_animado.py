# -*- encoding: utf-8 -*-
import pilasengine

pilas = pilasengine.iniciar()

class Protagonista(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = self.pilas.imagenes.cargar_animacion("pixel_player.png", 3)
        self.escala = 1

        self.imagen.definir_animacion("camina", [2, 1], 4)
        self.imagen.definir_animacion("parado", [0], 1)

        self.imagen.cargar_animacion('camina')

        self.escala_x = [2, 1] * 3, 1.25/3
        self.escala_y = [2, 1] * 3, 1.0/3
        self.rotacion = 128
        self.rotacion = [0], 0.5

    def actualizar(self):
        self.imagen.avanzar()


pilas.actores.vincular(Protagonista)
pilas.actores.Protagonista()

def crear_personaje(evento):
    p = pilas.actores.Protagonista()
    p.x = evento.x
    p.y = evento.y

pilas.eventos.click_de_mouse.conectar(crear_personaje)

pilas.fondos.Color(pilasengine.colores.gris)

pilas.avisar(u"Hacé click para crear mas personajes.")

pilas.ejecutar()