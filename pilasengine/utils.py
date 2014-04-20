# -*- encoding: utf-8 -*-
import os
import sys
import uuid

PATH = os.path.dirname(os.path.abspath(__file__))
INTERPRETE_PATH = os.path.dirname(sys.argv[0])

class Utils(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def obtener_uuid(self):
        """Genera un identificador único."""
        return str(uuid.uuid4())


def es_interpolacion(an_object):
    """Indica si un objeto se comportará como una interpolación.

    :param an_object: El objeto a consultar.
    """
    return isinstance(an_object, interpolaciones.Interpolacion)

def obtener_ruta_al_recurso(ruta):
    dirs = ['./', '/../data', 'data',
            PATH, INTERPRETE_PATH,
            PATH + '/data', INTERPRETE_PATH + '/data',
            PATH + '/../data', INTERPRETE_PATH + '/../data'
           ]

    for x in dirs:
        full_path = os.path.join(x, ruta)

        if os.path.exists(full_path):
            return full_path

    # Si no ha encontrado el archivo lo reporta.
    raise IOError("El archivo '%s' no existe." % (ruta))

def interpolable(f):
    """Decorador que se aplica a un metodo para que permita animaciones de interpolaciones.

    Ejemplo::

        @interpolable
        def set_x(self, valor_x):
            [...]

    :param f: Método sobre el que va a trabajar el interpolador.
    """

    def inner(*args, **kwargs):
        value = args[1]

        # Si le indican dos argumentos, el primer sera
        # el valor de la interpolacion y el segundo la
        # velocidad.
        if isinstance(value, tuple) and len(value) == 2:
            duracion = value[1]
            value = value[0]
        else:
            duracion = 1

        if isinstance(value, list):
            value = interpolar(value, duracion=duracion, tipo='lineal')
        elif isinstance(value, xrange):
            value = interpolar(list(value), duracion=duracion, tipo='lineal')

        if es_interpolacion(value):
            value.apply(args[0], function=f.__name__)
        else:
            f(args[0], value, **kwargs)

    return inner