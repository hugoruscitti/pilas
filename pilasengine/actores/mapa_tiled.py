# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os
from pilasengine.actores.mapa import Mapa
from xml.dom import minidom
import pilasengine

class MapaTiled(Mapa):
    """Representa mapas creados a partir de imagenes mas pequeñas.

    Este actor te permite crear escenarios tipo ``tiles``, a partir
    de archivos .tmx, creados con el programa **tiled** (ver http://www.mapeditor.org).

    Por ejemplo, para crear un mapa desde un archivo del programa
    **tiled** puedes escribir:

        >>> mapa = pilas.actores.MapaTiled('untitled2.tmx')

    Tiled trabaja con capas, así que cuando pilas carga las capas las interpreta
    de la siguiente manera:

        - Tos las capas se van a dibujar.
        - Toda capa que comienza con la palabra "solido" armará bloques con física y colisión.
    """

    def pre_iniciar(self, ruta_mapa=None, x=0, y=0, densidad=0, restitucion=0,
                          friccion=10.5, amortiguacion=0.1):
        pass

    def iniciar(self, ruta_mapa=None, x=0, y=0,
                densidad=0, restitucion=0, friccion=10.5, amortiguacion=0.1,
                reiniciar_si_cambia=True):
        self.actores_con_figuras_solidas = []
        ruta_mapa = self.pilas.obtener_ruta_al_recurso(ruta_mapa)
        self.ruta_mapa = ruta_mapa
        self.x = x
        self.y = y

        self.densidad = densidad
        self.restitucion = restitucion
        self.friccion = friccion
        self.amortiguacion = amortiguacion

        self._redibujar()
        self.radio_de_colision = 0

        if reiniciar_si_cambia:
            self.watcher = pilasengine.watcher.Watcher(ruta_mapa, self._redibujar)

    def _redibujar(self):
        self._eliminar_todos_los_actores_con_figuras()
        self._cargar_datos_basicos_del_mapa(self.ruta_mapa)
        Mapa.iniciar(self, self.x, self.y, self.grilla, filas=self.filas, columnas=self.columnas,
                        densidad=self.densidad, restitucion=self.restitucion,
                        friccion=self.friccion, amortiguacion=self.amortiguacion)
        self._dibujar_mapa(self.ruta_mapa)

    def cuadro_ancho(self):
        """Retorna el ancho de un bloque del mapa"""
        return self.ancho_cuadro

    def cuadro_alto(self):
        """Retorna el alto de un bloque del mapa"""
        return self.alto_cuadro

    def _cargar_datos_basicos_del_mapa(self, archivo):
        nodo = makeRootNode(archivo)

        # Analiza si el archivo es formato CSV
        layers = nodo.getChild('map').getChildren('layer')

        if len(layers) == 0:
            raise Exception("El mapa solicitado no tiene ninguna capa.")

        data = layers[0].getChildren('data')
        encoding = data[0].getAttributeValue('encoding')

        if encoding.lower() != 'csv':
            raise Exception("El formato de archivo es incorrecto. Selecciona CSV dentro de las preferencias de Tiled")

        nodo_mapa = nodo.getChild('map')
        nodo_tileset = nodo_mapa.getChild('tileset')

        self.columnas = int(nodo_mapa.getAttributeValue('width'))
        self.filas = int(nodo_mapa.getAttributeValue('height'))

        self.ancho_imagen = int(nodo_tileset.getChild('image').getAttributeValue('width'))
        self.alto_imagen = int(nodo_tileset.getChild('image').getAttributeValue('height'))

        self.ancho_cuadro = int(nodo_tileset.getAttributeValue('tilewidth'))
        self.alto_cuadro = int(nodo_tileset.getAttributeValue('tileheight'))

        ruta_a_imagen = nodo_tileset.getChild('image').getAttributeValue('source')

        # Convierte la ruta de la imagen a una ruta absoluta.
        ruta_actual = os.path.dirname(os.path.abspath(archivo))
        self._ruta = os.path.join(ruta_actual, ruta_a_imagen)
        self._ruta = self.pilas.obtener_ruta_al_recurso(self._ruta)
        self._ruta = unicode(self._ruta, encoding='utf-8')

        self.grilla = self.pilas.imagenes.cargar_grilla(self._ruta,
                self.ancho_imagen / self.ancho_cuadro,
                self.alto_imagen / self.alto_cuadro)

    def _dibujar_mapa(self, archivo):
        nodo = makeRootNode(archivo)
        layers = nodo.getChild('map').getChildren('layer')

        if len(layers) == 0:
            raise Exception("Debe tener al menos una capa (layer).")

        self.capas = {}

        # La capa 0 (inferior) define los bloques no-solidos.

        for (index, layer) in enumerate(layers):
            es_solido = layer.getAttributeValue('name').lower().startswith('solido')

            bloques = self._pintar_bloques(layer, solidos=es_solido)
            self.capas[index] = bloques

    def _pintar_bloques(self, capa, solidos):
        """Genera actores que representan los bloques del escenario.

        Retorna una lista de los bloques convertidos a numeros.
        """

        # Convierte todo el mapa en una matriz de numeros.
        bloques = self._convertir_capa_en_bloques_enteros(capa)

        for (y, fila) in enumerate(bloques):
            for (x, bloque) in enumerate(fila):
                if bloque:
                    self.pintar_bloque(y, x, bloque -1, solidos)

        return bloques

    def _convertir_capa_en_bloques_enteros(self, capa):
        datos = capa.getChild('data').getData()
        return [[int(x) for x in x.split(',') if x] for x in datos.split()]



class XmlNode:
    """Representa un nodo XML."""

    def __init__(self, domElement):
        """Construstor del nodo desde un elemento dom.

        :param domElement: Elemento de DOM a convertir.
        """
        self.elem = domElement

    def getData(self):
        """Extrae datos desde un nodo del DOM."""
        for child in self.elem.childNodes:
            if child.nodeType == child.TEXT_NODE:
                return str(child.data)
        return None

    def getAttributeValue(self, name):
        """Returns the value of the attribute having the specified name."""
        return str(self.elem.attributes[name].value)

    def getChild(self, tag):
        """Retorna el primer nodo hijo que contenga el tag especificado."""
        return XmlNode(self.elem.getElementsByTagName(tag)[0])

    def getChildren(self, tag):
        """Retorna una lista de todos los nodos hijos que tienen el tag especificado."""
        return [XmlNode(x) for x in self.elem.getElementsByTagName(tag)]

def makeRootNode(xmlFileName):
    """Genera un nodo XML dado un archivo.

    :param xmlFileName: El nombre del archivo .xml"""
    return XmlNode(minidom.parse(xmlFileName))
