# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
import random

FILAS = 4
COLUMNAS = 7

class Piezas(pilas.escenas.Normal):
    """Representa la escena de rompecabezas.

    La escena comienza con una imagen que se descompone en muchos
    actores Pieza.
    """

    def __init__(self, ruta_a_la_imagen="ejemplos/data/piezas.png"):
        pilas.escenas.Normal.__init__(self, pilas.colores.gris_oscuro)
        grilla = pilas.imagenes.Grilla(ruta_a_la_imagen, COLUMNAS, FILAS)
        self.piezas = []

        for x in range(FILAS * COLUMNAS):
            pieza = Pieza(self, grilla, x)
            pieza.x = random.randint(-200, 200)
            pieza.y = random.randint(-200, 200)

            self.piezas.append(pieza)



class Pieza(pilas.actores.Animacion):
    """Representa una pieza del rompecabezas.

    Esta pieza se puede arrastrar con el mouse y cuando se suelta
    intentará conectarse con las demás."""

    def __init__(self, escena_padre, grilla, cuadro):
        pilas.actores.Animacion.__init__(self, grilla)
        self.definir_cuadro(cuadro)
        self.radio_de_colision = 40
        self.escena_padre = escena_padre
        pilas.eventos.click_de_mouse.conectar(self.intentar_arrastrar)
        self.otras_piezas_conectadas = []

    def actualizar(self):
        pass

    def comienza_a_arrastrar(self):
        print self, "Me estan cambiando la posicion."

    def termina_de_arrastrar(self):
        # Busca todas las colisiones entre esta pieza
        # que se suelta y todas las demás.
        colisiones = pilas.colisiones.obtener_colisiones(self, self.escena_padre.piezas)

        print "Esta pieza colisiona con", colisiones


    def intentar_conectar(self, otra_pieza):
        self.conectar_con(otra_pieza)
        
    def conectar_con(self, otra_pieza):
        if otra_pieza not in self.otras_piezas_conectadas:
            self.otras_piezas_conectadas.append(otra_pieza)

            for x in otra_pieza.otras_piezas_conectadas:
                if x not in self.otras_piezas_conectadas:
                    self.otras_piezas_conectadas.append(x)

    def intentar_arrastrar(self, sender, signal, x, y, button):
        "Intenta mover el objeto con el mouse cuando se pulsa sobre el."

        if self.colisiona_con_un_punto(x, y):
            pilas.eventos.termina_click.connect(self.drag_end, uid='drag_end')
            pilas.eventos.mueve_mouse.connect(self.drag, uid='drag')
            self.last_x = x
            self.last_y = y
            self.comienza_a_arrastrar()

    def drag(self, sender, signal, x, y, dx, dy):
        "Arrastra el actor a la posicion indicada por el puntero del mouse."
        self.x += dx
        self.y += dy
        self.mover_las_piezas_conectadas(dx, dy)

    def mover_las_piezas_conectadas(self, dx, dy):
        for pieza in self.otras_piezas_conectadas:
            pieza.x += dx
            pieza.y += dy

    def drag_end(self, sender, signal, x, y, button):
        "Suelta al actor porque se ha soltado el botón del mouse."
        pilas.eventos.mueve_mouse.desconectar(uid='drag')
        pilas.eventos.mueve_mouse.desconectar(uid='drag_end')
        self.termina_de_arrastrar()

    def __repr__(self):
        return "<<Pieza %d>>" %(self.animacion.obtener_cuadro())
