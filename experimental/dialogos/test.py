# -*- encoding: utf-8 -*-
import pilas

class Globo(pilas.actores.Actor):

    def __init__(self, dialogo, texto, x=0, y=0):
        self.dialogo = dialogo
        pilas.actores.Actor.__init__(self, x=x, y=y)
        ancho, alto = self._crear_lienzo(texto, pilas) 
        imagen = pilas.imagenes.cargar_imagen_cairo("globo.png")

        self._pintar_globo(x, y, ancho, alto, imagen)
        self.lienzo.definir_color(pilas.colores.negro)
        self._escribir_texto(texto)
        self.lienzo.asignar(self)
        self.centro = ("derecha", "abajo")
        pilas.eventos.click_de_mouse.conectar(self.cuando_quieren_avanzar)

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


class GloboElegir(Globo):
    
    def __init__(self, dialogo, texto, opciones, funcion_a_invocar, x=0, y=0):
        self.dialogo = dialogo
        self.opciones = opciones
        self.funcion_a_invocar = funcion_a_invocar
        Globo.__init__(self, dialogo, texto, x, y)

    def _obtener_area_para_el_texto(self, texto):
        ancho, alto = self.lienzo.obtener_area_de_texto(texto, tamano=14)

        # Aumenta el tamano para las opciones
        for opcion in self.opciones:
            ancho_opcion, alto_opcion = self.lienzo.obtener_area_de_texto(opcion, tamano=14)
            ancho = max(ancho, ancho_opcion)
            alto += alto_opcion + 10

        return ancho, alto
        
    def _escribir_texto(self, texto):
        self.lienzo.escribir(texto, 12, 25, tamano=14)
        
        for (indice, respuesta) in enumerate(self.opciones):
            self.lienzo.escribir(respuesta, 12, 25 + 30 + indice * 20, tamano=14)    
    
    def cuando_quieren_avanzar(self, *k):
        print "No se puede avanzar..."
        
class Dialogo:
    "Representa una secuencia de mensajes entre varios actores."
    
    def __init__(self):
        self.dialogo = []
        self.dialogo_actual = None
    
    def decir(self, actor, texto):
        self.dialogo.append((actor, texto))
    
    def elegir(self, actor, texto, opciones, funcion_a_invocar):
        self.dialogo.append((actor, texto, opciones, funcion_a_invocar))
        
    def ejecutar(self, funcion):
        self.dialogo.append(funcion)

    def iniciar(self):
        self.avanzar_al_siguiente_dialogo()

    def obtener_siguiente_dialogo_o_funcion(self):
        if self.dialogo:
            return self.dialogo.pop(0)
        
    def _eliminar_dialogo_actual(self):
        if self.dialogo_actual:
            self.dialogo_actual.eliminar()
            self.dialogo_actual = None

    def _mostrar_o_ejecutar_siguiente(self, siguiente):
        if isinstance(siguiente, tuple):
            # Es un mensaje de dialogo simple
            if len(siguiente) == 2:
                actor, texto = siguiente
                self.dialogo_actual = Globo(self, texto, x=actor.x + 30, y=actor.y + 30)
            else:
                # Es un mensaje con seleccion.
                actor, texto, opciones, funcion_a_invocar = siguiente
                self.dialogo_actual = GloboElegir(self, texto, opciones, funcion_a_invocar, x=actor.x + 30, y=actor.y + 30)
        else:
            siguiente()

    def avanzar_al_siguiente_dialogo(self, evento=None):
        self._eliminar_dialogo_actual()
        siguiente = self.obtener_siguiente_dialogo_o_funcion()
        
        if siguiente:
            self._mostrar_o_ejecutar_siguiente(siguiente)
        else:
            print "Termino el dialogo."
            return False
            
        return True

pilas.iniciar()

# La secuencia es sencilla, el mono dice 'hola', 
mono = pilas.actores.Mono(x=-100)
mono_chiquito = pilas.actores.Mono(x=200)
mono_chiquito.escala = 0.75

"""
d = Dialogo()
d.decir(mono, "Hola, como estas?")
d.decir(mono_chiquito, "Bien, ¿y vos?...")
d.decir(mono, "Bien... ¡Mirá cómo salto !")

def hacer_que_el_mono_salte():
    mono.sonreir()
    mono.y = [300], 1

d.ejecutar(hacer_que_el_mono_salte)
d.decir(mono_chiquito, "wow...")
"""

d = Dialogo()
d.decir(mono, "¿Cual es tu color favorito?")

def cuando_responde_color_favorito(respuesta):
    d.decir(mono, "Ya esta, ahora tenemos fondo '%s" %(respuesta))
    d.decir(mono_chiquito, "fua...")
    
d.elegir(mono_chiquito, "Mi color favorito es el...", ["rojo", "verde", "azul"], cuando_responde_color_favorito)


d.iniciar()
pilas.avisar("Tienes que hacer click para que la animacion avance.")
pilas.ejecutar()