#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
from setuptools import setup

setup(
        name='pilas',
        zip_safe=False,
        version="1.4.9",
        description="""Pilas Engine - un motor para realizar videojuegos de manera rápida y sencilla.

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
            'pilasengine',
            'pilasengine.actores',
            'pilasengine.asistente',
            'pilasengine.colisiones',
            'pilasengine.comportamientos',
            'pilasengine.fisica',
            'pilasengine.datos',
            'pilasengine.fisica.constantes',
            'pilasengine.interprete',
            'pilasengine.interprete.editorbase',
            'pilasengine.tareas',
            'pilasengine.configuracion',
            'pilasengine.fondos',
            'pilasengine.manual',
            'pilasengine.tests',
            'pilasengine.actores',
            'pilasengine.controles',
            'pilasengine.musica',
            'pilasengine.utils',
            'pilasengine.asistente',
            'pilasengine.depurador',
            'pilasengine.pad',
            'pilasengine.colisiones',
            'pilasengine.ejemplos',
            'pilasengine.habilidades',
            'pilasengine.escenas',
            'pilasengine.imagenes',
            'pilasengine.eventos',
            'pilasengine.interfaz',
            'pilasengine.sonidos',
            'data',
        ],
        url='http://www.pilas-engine.com.ar',
        include_package_data = True,

        package_data = {
            'images': [ 'data/*' ]
        },

        scripts=['bin/pilasengine'],
)
