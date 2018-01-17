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

                    actor = fixture.userData.get('actor', None)

                    if actor and actor.fijo:
                        dx = self.pilas.camara.x
                        dy = self.pilas.camara.y
                    else:
                        dx = 0
                        dy = 0

                    self._poligono(painter, vertices, dx=dx, dy=dy, color=colores.blanco, grosor=grosor, cerrado=True)
                elif isinstance(shape, box2d.b2CircleShape):
                    (x, y) = cuerpo.transform * shape.pos * PPM

                    actor = fixture.userData.get('actor', None)

                    if actor and actor.fijo:
                        x += self.pilas.camara.x
                        y += self.pilas.camara.y

                    self._angulo(painter, x, y, - math.degrees(fixture.body.angle), shape.radius * PPM)
                    self._circulo(painter, x, y, shape.radius * PPM)
                else:
                    raise Exception("No puedo identificar el tipo de figura.")

        painter.restore()

    def _poligono(self, painter, puntos, dx=0, dy=0, color=colores.negro, grosor=1, cerrado=False):
        x, y = puntos[0]

        if cerrado:
            puntos.append((x, y))

        for p in puntos[1:]:
            nuevo_x, nuevo_y = p

            self._linea(painter, x+dx, y+dy, nuevo_x+dx, nuevo_y+dy)
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
