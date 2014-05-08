#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
from setuptools import setup

setup(
        name='pilas',
        zip_safe=False,
        version="0.9",
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
        packages=[
            'lanas',
            'pilasengine',
            'pilasengine.actores',
            'pilasengine.asistente',
            'pilasengine.depurador',
            'pilasengine.ejemplos',
            'pilasengine.escenas',
            'pilasengine.fondos',
            'pilasengine.imagenes',
            'pilasengine.interprete',
            'pilasengine.manual',
            'pilasengine.tests',
            'pilasengine.utils',
            ],
        url='http://www.pilas-engine.com.ar',
        include_package_data = True,
        package_data = {
            'images': ['data/*',
                       'data/fuentes/*',
                       'data/asistente',
                       ],
            },

        scripts=['bin/pilas.py'],

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

