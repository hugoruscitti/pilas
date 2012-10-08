#!/usr/bin/env python
from setuptools import setup
from lanas import version

setup(
        name='lanas',
        version=version.VERSION,
        description='Una consola sencilla de python',
        author='Hugo Ruscitti',
        include_package_data = True,
        package_data = {
        },
        url='https://github.com/hugoruscitti/lanas',
        scripts=['bin/lanas'],
        author_email='hugoruscitti@gmail.com',
        install_requires=['setuptools'],
        packages=['lanas'],
)
