# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
import random


class Piezas(pilas.escenas.Normal):
    """Representa la escena de rompecabezas.

    La escena comienza con una imagen que se descompone en muchos
    actores Pieza.
    """

    def __init__(self, ruta_a_la_imagen="ejemplos/data/piezas.png", filas=4, columnas=7):
        pilas.actores.eliminar_a_todos()
        pilas.escenas.Normal.__init__(self, pilas.colores.gris_oscuro)
        grilla = pilas.imagenes.Grilla(ruta_a_la_imagen, columnas, filas)
        self.crear_piezas(grilla, filas, columnas)

        pilas.eventos.click_de_mouse.conectar(self.al_hacer_click)

    def crear_piezas(self, grilla, filas, columnas):
        self.piezas = []

        for x in range(filas * columnas):
            pieza = Pieza(self, grilla, x)
            pieza.x = random.randint(-200, 200)
            pieza.y = random.randint(-200, 200)

            self.piezas.append(pieza)

    def al_hacer_click(self, *k, **kv):
        pieza_debajo_de_mouse = pilas.actores.obtener_actor_en(kv['x'], kv['y'])

        if pieza_debajo_de_mouse:
            pieza_debajo_de_mouse.al_recibir_un_click()



class Pieza(pilas.actores.Animacion):
    """Representa una pieza del rompecabezas.

    Esta pieza se puede arrastrar con el mouse y cuando se suelta
    intentará conectarse con las demás."""

    def __init__(self, escena_padre, grilla, cuadro):
        pilas.actores.Animacion.__init__(self, grilla)
        self.definir_cuadro(cuadro)

        self.radio_de_colision = 40
        self.escena_padre = escena_padre
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

    def al_recibir_un_click(self):
        "Intenta mover el objeto con el mouse cuando se pulsa sobre el."

        pilas.eventos.termina_click.connect(self.drag_end, uid='drag_end')
        pilas.eventos.mueve_mouse.connect(self.drag, uid='drag')
        self.last_x = self.x
        self.last_y = self.y
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
