# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
from pilas.actores import Mapa
from xml.dom import minidom

class MapaTiled(Mapa):
    """Representa mapas creados a partir de imagenes mas pequeñas.

    Este actor te permite crear escenarios tipo ``tiles``, a partir
    de archivos .tmx, creados con el programa **tiled** (ver http://www.mapeditor.org).

    Por ejemplo, para crear un mapa desde un archivo del programa
    **tiled** puedes escribir:

        >>> mapa = pilas.actores.MapaTiled('untitled2.tmx')

    Tiled trabaja con capas, así que cuando pilas carga las capas las interpreta
    de la siguiente manera:

        - La capa 0 define los bloques no sólidos, generalmente fondos o decoración.
        - La capa 1 define bloques sólidos, útiles para hacer suelos o paredes.
        - Las siguientes capas solo se almacenan, pero no se dibujan. Se pueden acceder con ``mapa.capas``.
    """

    def __init__(self, ruta_mapa, x=0, y=0, restitucion=0.56):
        ruta_mapa = pilas.utils.obtener_ruta_al_recurso(ruta_mapa)
        self._cargar_datos_basicos_del_mapa(ruta_mapa)
        Mapa.__init__(self, self.grilla, x=x, y=y, filas=self.filas, columnas=self.columnas)
        self._dibujar_mapa(ruta_mapa)

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

        self._ruta = nodo_tileset.getChild('image').getAttributeValue('source')
        self._ruta = pilas.utils.obtener_ruta_al_recurso(self._ruta)

        self.grilla = pilas.imagenes.cargar_grilla(self._ruta,
                self.ancho_imagen / self.ancho_cuadro,
                self.alto_imagen / self.alto_cuadro)

    def _dibujar_mapa(self, archivo):
        nodo = makeRootNode(archivo)
        layers = nodo.getChild('map').getChildren('layer')

        if len(layers) == 0:
            raise Exception("Debe tener al menos una capa (layer).")

        self.capas = {}

        # La capa 0 (inferior) define los bloques no-solidos.
        bloques = self._pintar_bloques(layers[0], solidos=False)
        self.capas[0] = bloques

        # La capa 1 define bloques solidos.
        if len(layers) > 1:
            bloques = self._pintar_bloques(layers[1], solidos=True)
            self.capas[1] = bloques

        # El resto de las capas solo definen matrices para acceder mediante
        # el atributo 'capas', no se imprimen automaticamente.
        for (indice, layer) in enumerate(layers[2:]):
            self.capas[indice + 2] = self._convertir_capa_en_bloques_enteros(layer)

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

