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
    de archivos .tmx, creados con el programa
    **tiled** (ver http://www.mapeditor.org).

    Por ejemplo, para crear un mapa desde un archivo del programa
    **tiled** puedes escribir:

        >>> mapa = pilas.actores.MapaTiled('untitled2.tmx')
    """

    def __init__(self, ruta_mapa, x=0, y=0, restitucion=0.56):
        ruta_mapa = pilas.utils.obtener_ruta_al_recurso(ruta_mapa)
        self._cargar_datos_basicos_del_mapa(ruta_mapa)
        Mapa.__init__(self, self.grilla, x=x, y=y, filas=self.filas, columnas=self.columnas)
        self._dibujar_mapa(ruta_mapa)

    def cuadro_ancho(self):
        return self.ancho_cuadro

    def cuadro_alto(self):
        return self.alto_cuadro

    def _cargar_datos_basicos_del_mapa(self, archivo):
        nodo = makeRootNode(archivo)
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
        nodo_mapa = nodo.getChild('map')
        nodo_tileset = nodo_mapa.getChild('tileset')

        layers = nodo.getChild('map').getChildren('layer')

        if len(layers) == 0:
            raise Exception("Debe tener al menos una capa (layer).")

        # La capa 0 (inferior) define los bloques no-solidos.
        self._pintar_bloques(layers[0], solidos=False)

        # El resto de las capas definen bloques solidos
        for layer in layers[1:]:
            self._pintar_bloques(layer, solidos=True)

    def _pintar_bloques(self, capa, solidos):
        "Genera actores que representan los bloques del escenario."
        datos = capa.getChild('data').getData()

        # Convierte todo el mapa en una matriz de numeros.
        bloques = [[int(x) for x in x.split(',') if x] for x in datos.split()]

        for (y, fila) in enumerate(bloques):
            for (x, bloque) in enumerate(fila):
                if bloque:
                    self.pintar_bloque(y, x, bloque -1, solidos)



class XmlNode:
    """An XML node represents a single field in an XML document."""

    def __init__(self, domElement):
        """Construct an XML node from a DOM element."""
        self.elem = domElement

    def getData(self):
        """Extract data from a DOM node."""
        for child in self.elem.childNodes:
            if child.nodeType == child.TEXT_NODE:
                return str(child.data)
        return None

    def getAttributeValue(self, name):
        """Returns the value of the attribute having the specified name."""
        return str(self.elem.attributes[name].value)

    def getChild(self, tag):
        """Returns the first child node having the specified tag."""
        return XmlNode(self.elem.getElementsByTagName(tag)[0])

    def getChildren(self, tag):
        """Returns a list of child nodes having the specified tag."""
        return [XmlNode(x) for x in self.elem.getElementsByTagName(tag)]


def makeRootNode(xmlFileName):
    """Creates the root node from an XML file."""
    return XmlNode(minidom.parse(xmlFileName))

