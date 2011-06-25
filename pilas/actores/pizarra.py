# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Actor

class Lapiz(object):

    def __init__(self):
        self.x = 0
        self.y = 0

    def set_x(self, x):
        self._x = x + 320

    def get_x(self):
        return self._x

    def set_y(self, y):
        self._y = 240 - y 

    def get_y(self):
        return self._y

    x = property(get_x, set_x)
    y = property(get_y, set_y)

class PizarraAbstracta():
    def __init__(self, ancho=640, alto=480):
        self.canvas = pilas.motor.obtener_canvas(ancho, alto)
        self.lapiz = Lapiz()

        self.levantar_lapiz()
        self.mover_lapiz(0, 0)

        self.actualizar_imagen()
        self.habilitar_actualizacion_automatica()        
        self.centro = ("medio", "medio")
                
    def asignar(self, actor):
        actor.imagen = self.canvas.image
        
    def levantar_lapiz(self):
        self.lapiz_bajo = False

    def bajar_lapiz(self):
        self.lapiz_bajo = True

    def pintar_punto(self, x, y, radio, color):
        y = 240 - y
        x += 320
        self.definir_color(color)
        self.canvas.context.arc(x, y, radio, 0, 2*3.1415)
        self.canvas.context.fill()
        if self.actualiza_automaticamente:
            self.actualizar_imagen()

        
    def mover_lapiz(self, x, y):
        if self.lapiz_bajo:
            self.canvas.context.move_to(self.lapiz.x, self.lapiz.y)
            self.canvas.context.set_line_width(3)
            self.lapiz.x = x
            self.lapiz.y = y
            self.canvas.context.line_to(self.lapiz.x, self.lapiz.y)
            self.canvas.context.stroke()

            # Actualiza la imagen si ha dibujado.
            if self.actualiza_automaticamente:
                self.actualizar_imagen()

        self.lapiz.x, self.lapiz.y = x, y
        
    def definir_color(self, color):
        b, g, r, a = color.obtener_componentes()
        
        self.canvas.context.set_source_rgb(r/255.0, g/255.0, b/255.0)

    def pintar_imagen(self, imagen, x=0, y=0):
        """Dibuja una imagen sobre la pizarra pero usando coordenadas de pantalla.

        Las coordenadas de pantalla tienen su origen en la esquina
        superior izquierda, no en el centro de la ventana.
        """
        
        if not isinstance(imagen, cairo.ImageSurface):
            imagen = pilas.motor.obtener_imagen_cairo(imagen)
            
        w = imagen.get_width()
        h = imagen.get_height()
        self.pintar_parte_de_imagen(imagen, 0, 0, w, h, x, y)

    def pintar_grilla(self, grilla, x=0, y=0):
        imagen = pilas.motor.obtener_imagen_cairo(grilla.image)
        w = grilla.cuadro_ancho
        h = grilla.cuadro_alto
        dx = grilla.obtener_dx()
        dy = grilla.obtener_dy()

        self.pintar_parte_de_imagen(imagen, dx, dy, w, h, x, y)

    def pintar_parte_de_imagen(self, imagen_cairo, origen_x, origen_y, ancho, alto, x, y):
        """Dibuja una porcion de imagen sobre la pizarra pero usando coordenadas de pantalla.

        Los argumentos ``origen_x`` y ``origen_y`` indican la parte
        izquierda de la imagen que se descartará, ``ancho`` y ``alto``
        el tamaño de rectángulo que se desea leer y por último ``x`` e ``y``
        son las coordenadas destino de impresión.

        Ten en cuenta que las coordenadas de pantalla tienen su origen en la esquina
        superior izquierda, no en el centro de la ventana.
        """

        self.canvas.context.set_source_surface(imagen_cairo, x - origen_x, y - origen_y)
        self.canvas.context.rectangle(x, y, ancho, alto)
        self.canvas.context.fill()
        if self.actualiza_automaticamente:
            self.actualizar_imagen()

    def pintar(self, color=None):
        w = self.canvas.surface.get_width()
        h = self.canvas.surface.get_height()

        if color:
            self.definir_color(color)

        self.canvas.context.rectangle(0, 0, w, h)
        self.canvas.context.fill()
        
        if self.actualiza_automaticamente:
            self.actualizar_imagen()

    def escribir(self, texto, x=0, y=0, tamano=32, fuente="sans"):
        "Pinta una cadena de texto con el color actual del trazo."
        self.canvas.context.move_to(x, y)
        self.canvas.context.set_font_size(tamano)
        self.canvas.context.select_font_face(fuente)
        self.canvas.context.show_text(texto)
        self.canvas.context.fill()

        if self.actualiza_automaticamente:
            self.actualizar_imagen()

    def obtener_area_de_texto(self, texto, tamano=32, fuente="sans"):
        """Retorna el tamano que tendra el texto una vez dibujado.
        
        El resultado es una tupla de tipo (ancho, alto)."""
        self.canvas.context.set_font_size(tamano)
        self.canvas.context.select_font_face(fuente)
        (_, _, ancho, alto, _, _) = self.canvas.context.text_extents(texto)
        return (ancho, alto)
    
    def obtener_area_para_lista_de_texto(self, lista, tamano=32, fuente="sans"):
        "Retorna el tamano que tendra una lista de cadenas de texto una vez dibujadas"
        ancho = 0
        alto = 0
        
        for opcion in lista:
            ancho_opcion, alto_opcion = self.obtener_area_de_texto(opcion, tamano=14, fuente=fuente)
            ancho = max(ancho, ancho_opcion)
            alto += alto_opcion + 10
    
        return ancho, alto

    def dibujar_rectangulo(self, x, y, ancho, alto, pintar=True):
        self.canvas.context.rectangle(x, y, ancho, alto)

        if pintar:
            self.canvas.context.fill()

        self.canvas.context.stroke()
        if self.actualiza_automaticamente:
            self.actualizar_imagen()

    def dibujar_poligono(self, puntos):
        (x, y) = puntos.pop(0)
        (x, y) = pilas.utils.hacer_coordenada_mundo(x, y)
        self.canvas.context.move_to(x, y)

        for (x, y) in puntos:
            (x, y) = pilas.utils.hacer_coordenada_mundo(x, y)
            self.canvas.context.line_to(x, y)
        
        self.canvas.context.close_path()
        self.canvas.context.stroke()
        
        if self.actualiza_automaticamente:
            self.actualizar_imagen()

    def pintar_cruz(self, x, y, ancho, color):
        self.definir_color(color)
        r = ancho
        self.dibujar_poligono([(x-r, y+r), (x+r,y-r)])
        self.dibujar_poligono([(x-r, y-r), (x+r,y+r)])
        
    def limpiar(self):
        self.canvas.limpiar()
        
        if self.actualiza_automaticamente:
            self.actualizar_imagen()
            
            
    def dibujar_circulo(self, x, y, radio, pintar=True):
        (x, y) = pilas.utils.hacer_coordenada_mundo(x, y)
        
        self.canvas.context.arc(x, y, radio, 0, 2*3.1415)
        
        if pintar:
            self.canvas.context.fill()
        else:
            self.canvas.context.stroke()
            
            
        if self.actualiza_automaticamente:
            self.actualizar_imagen()
            
            
class Pizarra(Actor):
    """Representa una superficie de dibujo inicialmente transparente.

    Puedes pintar sobre esta pizarra usando métodos que simulan
    un lapiz, que se puede mover sobre una superficie.
    """

    def __init__(self, x=0, y=0, ancho=None, alto=None):
        Actor.__init__(self, x=x, y=y)
        
    def definir_color(self, color):
        PizarraAbstracta.definir_color(self, color)
        
    def actualizar_imagen(self):
        "Se encarga de actualizar la vista de la pizarra."
        self.canvas.actualizar()
        self.definir_imagen(self.canvas.image)
