# -*- encoding: utf-8 -*-
import pilas

class Globo(pilas.actores.Actor):
    
    def __init__(self, texto, x=0, y=0):
        pilas.actores.Actor.__init__(self, x=x, y=y)
        ancho, alto = self._crear_lienzo(texto, pilas) 
        imagen = pilas.imagenes.cargar_imagen_cairo("globo.png")

        self._pintar_globo(x, y, ancho, alto, imagen)
        
        self.lienzo.definir_color(pilas.colores.negro)
        self.lienzo.escribir(texto, 12, 25, tamano=14)
        self.lienzo.asignar(self)
        self.centro = ("derecha", "abajo")

    def _crear_lienzo(self, texto, pilas):
        self.lienzo = pilas.lienzo.Lienzo(10, 10)
        ancho, alto = self.lienzo.obtener_area_de_texto(texto, tamano=14)
        ancho = int((ancho + 12) - (ancho % 12))
        alto = int((alto + 12) - alto % 12)
        self.lienzo = pilas.lienzo.Lienzo(ancho + 36, alto + 24 + 35)
        return ancho, alto

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


class Dialogo:
    
    def __init__(self):
        self.dialogo = []
        self.dialogo_actual = None
    
    def decir(self, actor, texto):
        self.dialogo.append((actor, texto))
        
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
            actor, texto = siguiente
            self.dialogo_actual = Globo(texto, x=actor.x + 30, y=actor.y + 30)
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

d = Dialogo()
d.decir(mono, "Hola, como estas?")
d.decir(mono_chiquito, "Bien, ¿y vos?...")
d.decir(mono, "Bien... ¡Mirá cómo salto !")

def hacer_que_el_mono_salte():
    mono.sonreir()
    mono.y = [300], 1

d.ejecutar(hacer_que_el_mono_salte)
d.decir(mono_chiquito, "wow...")


d.iniciar()
pilas.eventos.click_de_mouse.conectar(d.avanzar_al_siguiente_dialogo)

pilas.avisar("Tienes que hacer click para que la animacion avance.")
pilas.ejecutar()