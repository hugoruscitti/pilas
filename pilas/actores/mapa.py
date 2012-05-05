# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import copy
import math

import pilas
from pilas.actores import Actor

class Mapa(Actor):

    def __init__(self, grilla=None, x=0, y=0, filas=20, columnas=20):
        Actor.__init__(self, 'invisible.png', x, y)

        self.filas = filas
        self.columnas = columnas

        # Genera una matriz indicando cuales de los bloque son solidos.
        self.matriz_de_bloques = self._generar_matriz_de_bloques(filas, columnas)

        if not grilla:
            grilla = pilas.imagenes.cargar_grilla("grillas/plataformas_10_10.png", 10, 10)

        self.grilla = grilla
        self.superficie = pilas.imagenes.cargar_superficie(columnas * self.grilla.cuadro_ancho, filas * self.grilla.cuadro_alto)
        self.imagen = self.superficie

    def _generar_matriz_de_bloques(self, filas, columnas):
        cols = copy.copy([False] * columnas)
        matriz_de_bloques = []

        for indice_fila in range(filas):
            matriz_de_bloques.append(copy.copy(cols))

        return matriz_de_bloques

    def pintar_bloque(self, fila, columna, indice, es_bloque_solido=True):
        #self.matriz_de_bloques[fila][columna] = es_bloque_solido
        self.matriz_de_bloques[fila][columna] = es_bloque_solido

        # Definimos el cuadro que deseamos dibujar en la Superficie.
        self.grilla.definir_cuadro(indice)

        # Dibujamos el cuadro de la grilla en la Superficie.
        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto

        x = columna * ancho
        y = fila * alto

        self.grilla.dibujarse_sobre_una_pizarra(self.superficie, x, y)

    def pintar_limite_de_bloques(self):
        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto

        for fila in range(self.filas):
            for columna in range(self.columnas):
                self._pintar_borde_de_grilla(fila, columna)

    def _pintar_borde_de_grilla(self, fila, columna):
        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto
        x = columna * ancho
        y = fila * alto

        self.superficie.rectangulo(x+1, y+1, ancho-2, alto-2)

        texto_coordenada = "%d, %d" %(fila, columna)
        self.superficie.texto(texto_coordenada, x+3, y-3 + alto, magnitud=8)

    def obtener_distancia_al_suelo(self, x, y, maximo):
        """Retorna la distancia en pixels desde un punto del mundo al suelo.

        Es importante mostrar que las coordenadas x e y son coordenadas del
        mundo, no coordenadas de mouse o relativas al mapa.

        El argumento maximo es la cantidad de pixels que tomaremos como
        valor limite de la busqueda. Por ejemplo, si colocamos 100 como
        limite y la funcion nos retorna 100 es porque no encontró un suelo
        a menos de 100 pixels. Este límite existe por una cuestión de
        eficiencia."""

        # TODO: se puede hacer mas eficiente el algoritmo si en lugar
        #       de recorrer desde 0 a maximo solamente se recorre dando
        #       saltos por bloques (de 'self.grilla.cuadro_alto' pixels)
        try:
            x, y = self.convertir_de_coordenada_absoluta_a_coordenada_mapa(x, y)

            # El 'resto' es la coordenada 'y' interna a ese tile dentro
            # del mapa.
            resto = int(y % self.grilla.cuadro_alto)

            if not resto and self.es_punto_solido_coordenada_mapa(x, y):
                return 0

            # Es la distancia en pixels a la siguiente fila que se
            # tiene que evaluar.
            inicial = self.grilla.cuadro_alto - resto

            # Recorre el escenario hacia abajo, saltando por las filas
            # del mapa. Si encuentra un suelo se detiene y retorna la
            # cantidad de pixels que recorrió.
            for distancia in range(inicial, maximo, self.grilla.cuadro_alto):
                if self.es_punto_solido_coordenada_mapa(x, y+distancia):
                    return distancia

        except Exception as a:
            return maximo

        return maximo

    def es_bloque_solido(self, fila, columna):
        if not 0 <= fila < self.filas or not 0 <= columna < self.columnas:
            raise Exception("La fila y columna consultadas estan fuera del area del mapa.")

        return self.matriz_de_bloques[fila][columna]

    def es_punto_solido(self, x, y):
        # Los parametros x e y son coordenadas del escenario,
        # lo que se conoce como coordenanadas absolutas.

        # La siguiente conversión pasa esas coordenadas absolutas
        # a coordenadas del mapa, es decir, donde el punto (0, 0)
        # es la esquina superior izquierda del mapa.
        x, y = self.convertir_de_coordenada_absoluta_a_coordenada_mapa(x, y)
        return self.es_punto_solido_coordenada_mapa(x, y)

    def convertir_de_coordenada_absoluta_a_coordenada_mapa(self, x, y):
        dx, dy = self.centro
        x = x + dx - self.x
        y = -y + dy + self.y
        return x, y

    def es_punto_solido_coordenada_mapa(self, x, y):
        fila = self.obtener_numero_de_fila(y)
        columna = self.obtener_numero_de_columna(x)
        return self.es_bloque_solido(fila, columna)

    def obtener_numero_de_fila(self, y):
        # 'y' tiene que ser una coordenada del mapa
        return self._convertir_en_int(y / self.grilla.cuadro_alto)

    def obtener_numero_de_columna(self, x):
        # 'x'tiene que ser una coordenada del mapa
        return self._convertir_en_int(x / self.grilla.cuadro_ancho)

    def _convertir_en_int(self, valor):
        return int(math.floor(valor))
