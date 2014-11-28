#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
from setuptools import setup

from pilas import pilasversion


def error(biblioteca, web):
    print("Lo siento, no se encuentra la biblioteca '%s' (de %s)" %(biblioteca, web))
    print("Vea las instrucciones de instalación en: https://github.com/hugoruscitti/pilas")
    print("Se cancela la inicialización.")
    sys.exit(1)


def verificar_submodulos():
    if not os.path.exists('lanas/setup.py'):
        print("Lo siento, el modulo 'lanas' no existe.")
        print("Puede reparar el problema ejecutando el comando:\n\tgit submodule update --init")
        sys.exit(1)


verificar_submodulos()

try:
    import Box2D_23
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
            'box2d_23',
            ],
        packages=['pilas',
                  'pilas.actores',
                  'pilas.motores',
                  'pilas.demos',
                  'pilas.escena',
                  'pilas.ejemplos',
                  'pilas.interfaz',
	          'pilas.video',
                  'lanas.lanas',
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
     data_files=[('/usr/share/applications', ('debian/pilas.desktop',)),
		  ('/usr/share/pixmaps', ('debian/pilas-icono.png',))
         ]
    )

