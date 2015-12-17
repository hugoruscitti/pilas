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
    """Representa una mapa de bloques rectangulares, ideal para crear escenarios de plataformas
    y mapas.
    """


    def __init__(self, grilla=None, x=0, y=0, filas=20, columnas=20):
        """Inicializa el mapa.

        :param grilla: La imagen a utilizar cómo grilla con los bloques del escenario.
        :param x: Posición horizontal del mapa.
        :param y: Posición vertical del mapa.
        :param filas: Cantidad de filas que tendrá el mapa.
        :param columnas: Cantidad de columnas que tendrá el mapa.
        """
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
        self.centro_mapa_x, self.centro_mapa_y = self.superficie.centro()

        self.fijo = False

    def _generar_matriz_de_bloques(self, filas, columnas):
        cols = copy.copy([False] * columnas)
        matriz_de_bloques = []

        for indice_fila in range(filas):
            matriz_de_bloques.append(copy.copy(cols))

        return matriz_de_bloques

    def pintar_bloque(self, fila, columna, indice, es_bloque_solido=True):
        """Define un bloque de la grilla.

        :param fila: La fila que se definirá (comenzando desde 0).
        :param columna: La columna que se definirá (comenzando desde 0).
        :param indice: El número de cuadro referente a la grilla (comenzando desde 0).
        :param es_bloque_solido: True o False para indicar si los objetos físicos deberán colisionar con este bloque.
        """
        #self.matriz_de_bloques[fila][columna] = es_bloque_solido
        self.matriz_de_bloques[fila][columna] = es_bloque_solido

        # Definimos el cuadro que deseamos dibujar en la Superficie.
        self.grilla.definir_cuadro(indice)

        # Dibujamos el cuadro de la grilla en la Superficie.
        ancho = self.grilla.cuadro_ancho
        alto = self.grilla.cuadro_alto

        x = columna * ancho
        y = fila * alto

        #(dx, dy) = pilas.mundo.motor.centro_fisico()
        #actor = pilas.actores.Actor(x=x-dx+(ancho/2), y=dy-y-(alto/2))

        #actor.imagen = self.grilla.obtener_imagen_cuadro()
        self.grilla.dibujarse_sobre_una_pizarra(self.superficie, x, y)

    def pintar_limite_de_bloques(self):
        """Dibuja los bordes de cada bloque."""
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
        eficiencia.

        :param x: Posición horizontal de referencia.
        :param y: Posición vertical de referencia.
        :param maximo: Cantidad máxima de pixels a leer.
        """

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

        except Exception:
            return maximo

        return maximo

    def es_bloque_solido(self, fila, columna):
        """Indica si un determinado bloque es solido.

        Los bloques sólidos se utilizan para marcar paredes y plataformas, es
        decir que son bloques que generalmente no se pueden sobrepasar.

        :param fila: La fila que se observará.
        :param columna: La columna que se observará.
        """
        if not 0 <= fila < self.filas or not 0 <= columna < self.columnas:
            return True
            raise Exception("La fila y columna consultadas estan fuera del area del mapa.")

        return self.matriz_de_bloques[fila][columna]

    def es_punto_solido(self, x, y):
        """Indica si una coordenada del escenario está sobre un bloque solido.

        :param x: Posición horizontal a consultar.
        :param y: Posición vertical a consultar.

        """
        # Los parametros x e y son coordenadas del escenario,
        # lo que se conoce como coordenanadas absolutas.

        # La siguiente conversión pasa esas coordenadas absolutas
        # a coordenadas del mapa, es decir, donde el punto (0, 0)
        # es la esquina superior izquierda del mapa.
        x, y = self.convertir_de_coordenada_absoluta_a_coordenada_mapa(x, y)
        return self.es_punto_solido_coordenada_mapa(x, y)

    def convertir_de_coordenada_absoluta_a_coordenada_mapa(self, x, y):
        """Toma un punto de pantalla y lo convierte a una coordenada dentro del mapa.

        :param x: Coordenada horizontal de pantalla.
        :param y: Coordenada vertical de pantalla.
        """
        try:
            dx = self.centro[0]
            dy = self.centro[1]
            x = x + dx - self.x
            y = -y + dy + self.y
        except Exception as e:
            print(e)
        return x, y

    def es_punto_solido_coordenada_mapa(self, x, y):
        """Consulta si un punto (x, y) está señalando un bloque sólido.

        :param x: Coordenada horizontal.
        :param y: Coordenada vertical.
        """
        fila = self.obtener_numero_de_fila(y)
        columna = self.obtener_numero_de_columna(x)
        return self.es_bloque_solido(fila, columna)

    def obtener_numero_de_fila(self, y):
        """Retorna el número de fila correspondiente a una coordenada vertical.

        :param y: La coordenada vertical (relativa al mapa, no a la pantalla).
        """
        # 'y' tiene que ser una coordenada del mapa
        return self._convertir_en_int(y / self.grilla.cuadro_alto)

    def obtener_numero_de_columna(self, x):
        """Retorna el número de columna correspondiente a una coordenada horizontal.

        :param x: La coordenada horizontal (relativa al mapa, no a la pantalla).
        """
        # 'x'tiene que ser una coordenada del mapa
        return self._convertir_en_int(x / self.grilla.cuadro_ancho)

    def _convertir_en_int(self, valor):
        return int(math.floor(valor))
