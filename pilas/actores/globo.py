# -*- encoding: utf-8 -*-
import pilas
from pilas.actores import Actor

class Globo(Actor):
    "Representa un cuadro de dialogo estilo historietas."

    def __init__(self, texto, x=0, y=0, dialogo=None):
        self.dialogo = dialogo
        Actor.__init__(self, x=x, y=y)
        ancho, alto = self._crear_lienzo(texto, pilas) 
        imagen = pilas.imagenes.cargar_imagen_cairo("globo.png")

        self._pintar_globo(x, y, ancho, alto, imagen)
        self.lienzo.definir_color(pilas.colores.negro)
        self._escribir_texto(texto)
        self.lienzo.asignar(self)
        self.centro = ("centro", "centro")

        pilas.eventos.click_de_mouse.conectar(self.cuando_quieren_avanzar)

    def colocar_origen_del_globo(self, x, y):
        "Cambia la posicion del globo para que el punto de donde se emite el globo sea (x, y)."
        self.x = x - self.obtener_ancho() / 2 + 30
        self.y = y + self.obtener_alto() / 2
    

    def cuando_quieren_avanzar(self, *k):
        if self.dialogo:
            self.dialogo.avanzar_al_siguiente_dialogo()
            
    def _escribir_texto(self, texto):
        return self.lienzo.escribir(texto, 12, 25, tamano=14)
    
    def _crear_lienzo(self, texto, pilas):
        self.lienzo = pilas.lienzo.Lienzo(10, 10)
        ancho, alto = self._obtener_area_para_el_texto(texto)
        ancho = int((ancho + 12) - (ancho % 12))
        alto = int((alto + 12) - alto % 12)
        self.lienzo = pilas.lienzo.Lienzo(ancho + 36, alto + 24 + 35)
        return ancho, alto

    def _obtener_area_para_el_texto(self, texto):
        return self.lienzo.obtener_area_de_texto(texto, tamano=14)

    def _pintar_globo(self, x, y, ancho, alto, imagen):
        # esquina sup-izq
        self.lienzo.pintar_parte_de_imagen(imagen, 0, 0, 12, 12, 0, 0)
        # borde superior
        for x in range(0, int(ancho) + 12, 12):
            self.lienzo.pintar_parte_de_imagen(imagen, 12, 0, 12, 12, 12 + x, 0)
        
         # esquina sup-der
        self.lienzo.pintar_parte_de_imagen(imagen, 100, 0, 12, 12, 12 + int(ancho) + 12, 0)
        # centro del dialogo
        for y in range(0, int(alto) + 12, 12):
            # borde izquierdo
            self.lienzo.pintar_parte_de_imagen(imagen, 0, 12, 12, 12, 0, 12 + y)
            # linea horizontal blanca, para el centro del dialogo.
            for x in range(0, int(ancho) + 12, 12):
                self.lienzo.pintar_parte_de_imagen(imagen, 12, 12, 12, 12, 12 + x, 12 + y)
            
            # borde derecho
            self.lienzo.pintar_parte_de_imagen(imagen, 100, 12, 12, 12, 12 + int(ancho) + 12, 12 + y)
        
         # parte inferior
        self.lienzo.pintar_parte_de_imagen(imagen, 0, 35, 12, 12, 0, 0 + int(alto) + 12 + 12)
        # linea horizontal de la parte inferior
        for x in range(0, int(ancho) + 12, 12):
            self.lienzo.pintar_parte_de_imagen(imagen, 12, 35, 12, 12, 12 + x, 0 + int(alto) + 12 + 12)
        
        self.lienzo.pintar_parte_de_imagen(imagen, 100, 35, 12, 12, 12 + int(ancho) + 12, 0 + int(alto) + 12 + 12)
        # Pico de la parte de abajo
        self.lienzo.pintar_parte_de_imagen(imagen, 67, 35, 33, 25, int(ancho) - 12, 0 + int(alto) + 12 + 12)
