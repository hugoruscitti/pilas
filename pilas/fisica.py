# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


import pymunk


class Fisica:
    "Representa el motor de simulacion fisica."

    def __init__(self):
        pymunk.init_pymunk()

        self.espacio = pymunk.Space()
        self.espacio.gravity = (0.0, -900.0)
        self._crear_suelos()

    def _crear_suelos(self):
        static_body = pymunk.Body(pymunk.inf, pymunk.inf)
        static_lines = [
                        # Borde inferior
                        pymunk.Segment(static_body, (-320.0, -240.0), (320.0, -240.0), 0.0),
                        # Borde izquierdo
                        pymunk.Segment(static_body, (-320.0, 240.0), (-320.0, -240.0), 0.0),
                        # Borde izquierdo
                        pymunk.Segment(static_body, (320.0, 240.0), (320.0, -240.0), 0.0),
                        # Borde superior
                        pymunk.Segment(static_body, (-320.0, 240.0), (320.0, 240.0), 0.0),
                        ]

        for line in static_lines:
            line.elasticity = 20

        self.espacio.add_static(static_lines)


    def actualizar(self):
        self.espacio.step(1/50.0)

    def agregar(self, figura):
        self.espacio.add(figura)

    def crear_figura_circulo(self, x, y, radio, masa=1, elasticidad=0.05, friccion=0.05):
        inertia = pymunk.moment_for_circle(masa, 0, radio, (0,0))
        body = pymunk.Body(masa, inertia)
        body.position = x, y
        shape = pymunk.Circle(body, radio)
        shape.elasticity = elasticidad
        shape.friction = friccion
        self.espacio.add(body, shape)
        return shape

fisica = Fisica()
