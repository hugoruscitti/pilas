#!/usr/bin/env python
import sys
from setuptools import setup
from setuptools import find_packages
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
        version=pilasversion.VERSION,
        description='A simple to use video game framework.',
        author='Hugo Ruscitti',
        author_email='hugoruscitti@gmail.com',
        install_requires=[
            'setuptools',
            ],
        packages=['pilas', 'pilas.actores', 'pilas.dispatch', 
                  'pilas.motores', 'pilas.console',
                  'pilas.ejemplos',
                  'pilas.interfaz', 'pilas.video'],
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
            'Topic :: Education',
            'Topic :: Software Development :: Libraries',
          ],
    )

