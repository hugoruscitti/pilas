# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import math
import Box2D as box2d

from pilasengine.depurador.modo import ModoDepurador
from pilasengine import colores

PPM = 30

class ModoFisica(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def realizar_dibujado(self, painter):
        grosor = 1
        cuerpos = self.pilas.fisica.mundo.bodies

        painter.save()
        self.pilas.camara.aplicar_transformaciones_completas(painter)
        
        for cuerpo in cuerpos:

            for fixture in cuerpo:

                # cuerpo.type == 0 → estatico
                # cuerpo.type == 1 → kinematico
                # cuerpo.type == 2 → dinamico

                if fixture.userData['sensor']:
                    if cuerpo.awake:
                        self._definir_trazo_verde(painter)
                    else:
                        self._definir_trazo_verde_oscuro(painter)
                else:
                    if cuerpo.awake:
                        self._definir_trazo_blanco(painter)
                    else:
                        self._definir_trazo_gris(painter)

                shape = fixture.shape

                if isinstance(shape, box2d.b2PolygonShape):
                    vertices = [cuerpo.transform * v * PPM for v in shape.vertices]
                    #vertices = [pilas.escena_actual().camara.desplazar(v) for v in vertices]
                    #self._poligono(vertices, color=colores.negro, grosor=grosor+2, cerrado=True)
                    self._poligono(painter, vertices, color=colores.blanco, grosor=grosor, cerrado=True)
                elif isinstance(shape, box2d.b2CircleShape):
                    (x, y) = cuerpo.transform * shape.pos * PPM
                    #(x, y) = pilas.escena_actual().camara.desplazar(cuerpo.transform * shape.pos * PPM)

                    # Dibuja el angulo de la circunferencia.
                    self._angulo(painter, x, y, - math.degrees(fixture.body.angle), shape.radius * PPM)
                    #lienzo.angulo(motor, x, y, - math.degrees(fixture.body.angle), shape.radius * PPM, pilas.colores.blanco, grosor=grosor)

                    # Dibuja el borde de la circunferencia.
                    self._circulo(painter, x, y, shape.radius * PPM)
                    #lienzo.circulo(motor, x, y, shape.radius * PPM, pilas.colores.negro, grosor=grosor+2)
                    #lienzo.circulo(motor, x, y, shape.radius * PPM, pilas.colores.blanco, grosor=grosor)
                else:
                    # TODO: implementar las figuras de tipo "edge" y "loop".
                    raise Exception("No puedo identificar el tipo de figura.")

        painter.restore()

    def _poligono(self, painter, puntos, color=colores.negro, grosor=1, cerrado=False):
        x, y = puntos[0]

        if cerrado:
            puntos.append((x, y))

        for p in puntos[1:]:
            nuevo_x, nuevo_y = p
            self._linea(painter, x, y, nuevo_x, nuevo_y)
            x, y = nuevo_x, nuevo_y

    def _linea(self, painter, x0, y0, x1, y1):
        x0, y0 = self.hacer_coordenada_pantalla_absoluta(x0, y0)
        x1, y1 = self.hacer_coordenada_pantalla_absoluta(x1, y1)

        painter.drawLine(x0, y0, x1, y1)

    def hacer_coordenada_pantalla_absoluta(self, x, y):
        dx = -self.pilas.camara.x
        dy = self.pilas.camara.y
        return (x + dx, dy - y)

    def _angulo(self, painter, x, y, angulo, radio):
        angulo_en_radianes = math.radians(-angulo)
        dx = math.cos(angulo_en_radianes) * radio
        dy = math.sin(angulo_en_radianes) * radio
        self._linea(painter, x, y, x + dx, y + dy)

    def _circulo(self, painter, x, y, radio):
        x, y = self.hacer_coordenada_pantalla_absoluta(x, y)

        #r, g, b, a = color.obtener_componentes()
        #color = QtGui.QColor(r, g, b)
        #pen = QtGui.QPen(color, grosor)
        #painter.setPen(pen)

        painter.drawEllipse(x-radio+1, y-radio+1, radio*2, radio*2)
