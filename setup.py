#!/usr/bin/env python
from setuptools import setup
from lanas import version

setup(
        name='lanas',
        version=version.VERSION,
        description='Una consola sencilla de python',
        author='Hugo Ruscitti',
        author_email='hugoruscitti@gmail.com',
        install_requires=['setuptools'],
        packages=['lanas'],
)
