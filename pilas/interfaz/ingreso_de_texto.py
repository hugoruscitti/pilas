# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
import re

class IngresoDeTexto(pilas.actores.Actor):
    
    def __init__(self, texto_inicial="", x=0, y=0, ancho=300, limite_de_caracteres=20):
        pilas.actores.Actor.__init__(self, x=x, y=y)
        self.texto = texto_inicial
        self.cursor = "|"
        self.area_ancho = ancho
        self._cargar_lienzo()
        self._cargar_imagenes(pilas)
        self._actualizar_imagen()

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_una_tecla)
        pilas.mundo.agregar_tarea_siempre(0.25, self._actualizar_cursor)
        self.cualquier_caracter()
        self.limite_de_caracteres = limite_de_caracteres
        
    def _actualizar_cursor(self):
        if self.cursor == "":
            self.cursor = "|"
        else:
            self.cursor = ""
            
        self._actualizar_imagen()
        return True

    def cualquier_caracter(self):
        self.caracteres_permitidos = re.compile(".*")

    def solo_numeros(self):
        self.caracteres_permitidos = re.compile("\d+")

    def solo_letras(self):
        self.caracteres_permitidos = re.compile("[a-z]+")
        
    def _cargar_imagenes(self, pilas):
        self.imagen_caja = pilas.imagenes.cargar_imagen_cairo("interfaz/caja.png")
        
    def cuando_pulsa_una_tecla(self, evento):
        if evento.codigo == '\x08':
            # Indica que se quiere borrar un caracter
            self.texto = self.texto[:-1]
        else:

            if len(self.texto) < self.limite_de_caracteres:
                nuevo_texto = self.texto + evento.codigo

                if (self.caracteres_permitidos.match(evento.codigo)):
                    self.texto = self.texto + evento.codigo
                else:
                    print "Rechazando el ingreso del caracter:", evento.codigo
            else:
                print "Rechazando caracter por llegar al limite."
        
        self._actualizar_imagen()
        
    def _cargar_lienzo(self):
        self.lienzo = pilas.imagenes.cargar_lienzo(self.area_ancho + 33 + 40, 30)
        
    def _actualizar_imagen(self):
        #self.lienzo.pintar_imagen(self.imagen_caja)
        self.lienzo.pintar_parte_de_imagen(self.imagen_caja, 0, 0, 40, 30, 0, 0)
        self.centro = ("centro", "centro")

        for x in range(40, self.area_ancho - 40):
            self.lienzo.pintar_parte_de_imagen(self.imagen_caja, self.area_ancho - 40, 0, 40, 30, x, 0)

        self.lienzo.pintar_parte_de_imagen(self.imagen_caja, 333 - 40, 0, 40, 30, x+40, 0)
        self.lienzo.definir_color(pilas.colores.negro)
        self.lienzo.escribir(self.texto + self.cursor, 35, 20, tamano=14, fuente='sans')

        self.lienzo.asignar(self)
