#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
from setuptools import setup
from pilas import pilasversion


def error(biblioteca, web):
    print "Error, no se encuentra la biblioteca '%s' (de %s)" %(biblioteca, web)
    sys.exit(1)


try:
    import Box2D
except ImportError:
    error("box2d", "http://code.google.com/p/pybox2d")


setup(
        name='pilas',
	zip_safe=False,
        version=pilasversion.VERSION,
        description="""============
Pilas Engine
============

Pilas es un motor para realizar videojuegos de manera
rápida y sencilla.

Es una herramienta orientada a programadores casuales
o principiantes, que quiera comenzar a realizar sus
primeros videojuegos.

http://www.pilas-engine.com.ar
""",
        author='Hugo Ruscitti',
        author_email='hugoruscitti@gmail.com',
        install_requires=[
            'setuptools',
            'box2d',
            ],
        packages=['pilas',
                  'pilas.actores',
                  'pilas.motores',
                  'pilas.demos',
                  'pilas.escena',
                  'pilas.ejemplos',
                  'pilas.interfaz',
	              'pilas.video',
                  'lanas',
                  ],
        url='http://www.pilas-engine.com.ar',
        include_package_data = True,
        package_data = {
            'images': ['pilas/data/*', 'pilas/ejemplos/data/*',
                       'pilas/data/fondos/*', 'pilas/data/juegobase/*',
                       'pilas/data/juegobase/data/*',
                       'pilas/ejemplos/data',
                       'pilas/ejemplos/ejemplos',
                       ],
            },

        scripts=['bin/pilas'],

        classifiers = [
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
            'Natural Language :: Spanish',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Games/Entertainment',
          ],
    )

