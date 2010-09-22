#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages


setup(
        name='pilas',
        version='0.25',
        description='A simple to use video game framework.',
        author='Hugo Ruscitti',
        author_email='hugoruscitti@gmail.com',
        packages=['pilas', 'pilas.actores', 'pilas.dispatch'],
        url='http://www.pilas-engine.com.ar',

        include_package_data = True,
        package_data = {
            '': ['data/*'],
            },

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

