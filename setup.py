#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages


setup(
        name='pilas',
        version='0.2',
        description='A simple to use video game framework.',
        author='Hugo Ruscitti',
        author_email='hugoruscitti@gmail.com',
        packages=['pilas', 'pilas.dispatch'],

        include_package_data = True,
        package_data = {
            '': ['data/*'],
            },

        data_files=[('bitmaps', ['pilas/data/ejes.png'])]
        #scripts=['pilas'],
    )

