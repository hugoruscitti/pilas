# -*- encoding: utf-8 -*-
import pilas
from pilas.actores import Actor

class Globo(Actor):
    "Representa un cuadro de dialogo estilo historietas."

    def __init__(self, texto, x=0, y=0, dialogo=None, avance_con_clicks=True, autoeliminar=False):
        self.dialogo = dialogo
        Actor.__init__(self, imagen='invisible.png', x=x, y=y)

        ancho, alto = pilas.utils.obtener_area_de_texto(texto)

        ancho = int((ancho + 12) - (ancho % 12))
        alto = int((alto + 12) - alto % 12)

        self.imagen = pilas.imagenes.cargar_superficie(ancho + 36, alto + 24 + 35)

        self._pintar_globo(ancho, alto)
        self.imagen.texto(texto, 17, 30)
        self.centro = ("derecha", "abajo")
        self.escala = 0.1
        self.escala = [1], 0.2

        if avance_con_clicks:
            pilas.eventos.click_de_mouse.conectar(self.cuando_quieren_avanzar)

        if autoeliminar:
            pilas.mundo.tareas.una_vez(3, self.eliminar)

    def colocar_origen_del_globo(self, x, y):
        "Cambia la posicion del globo para que el punto de donde se emite el globo sea (x, y)."
        self.x = x
        self.y = y
    

    def cuando_quieren_avanzar(self, *k):
        if self.dialogo:
            self.dialogo.avanzar_al_siguiente_dialogo()
        else:
            self.eliminar()
            
    def _pintar_globo(self, ancho, alto):
        imagen = pilas.imagenes.cargar("globo.png")

        # esquina sup-izq
        self.imagen.pintar_parte_de_imagen(imagen, 0, 0, 12, 12, 0, 0)

        # borde superior
        for x in range(0, int(ancho) + 12, 12):
            self.imagen.pintar_parte_de_imagen(imagen, 12, 0, 12, 12, 12 + x, 0)
        
         # esquina sup-der
        self.imagen.pintar_parte_de_imagen(imagen, 100, 0, 12, 12, 12 + int(ancho) + 12, 0)

        # centro del dialogo
        for y in range(0, int(alto) + 12, 12):
            # borde izquierdo
            self.imagen.pintar_parte_de_imagen(imagen, 0, 12, 12, 12, 0, 12 + y)
            # linea horizontal blanca, para el centro del dialogo.
            for x in range(0, int(ancho) + 12, 12):
                self.imagen.pintar_parte_de_imagen(imagen, 12, 12, 12, 12, 12 + x, 12 + y)
            
            # borde derecho
            self.imagen.pintar_parte_de_imagen(imagen, 100, 12, 12, 12, 12 + int(ancho) + 12, 12 + y)
        
        # parte inferior
        self.imagen.pintar_parte_de_imagen(imagen, 0, 35, 12, 12, 0, 0 + int(alto) + 12 + 12)

        # linea horizontal de la parte inferior
        for x in range(0, int(ancho) + 12, 12):
            self.imagen.pintar_parte_de_imagen(imagen, 12, 35, 12, 12, 12 + x, 0 + int(alto) + 12 + 12)
        
        self.imagen.pintar_parte_de_imagen(imagen, 100, 35, 12, 12, 12 + int(ancho) + 12, 0 + int(alto) + 12 + 12)
        # Pico de la parte de abajo
        self.imagen.pintar_parte_de_imagen(imagen, 67, 35, 33, 25, int(ancho) - 12, 0 + int(alto) + 12 + 12)

    def eliminar(self):
        Actor.eliminar(self)
