# -*- encoding: utf-8 -*-
import os
import sys
import uuid
#import interpolaciones

import pitweener

from PyQt4 import QtGui

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
INTERPRETE_PATH = os.path.dirname(sys.argv[0])

class Utils(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def obtener_uuid(self):
        """Genera un identificador único."""
        return str(uuid.uuid4())

    def es_interpolacion(self, valor):
        return isinstance(valor, list) or (isinstance(valor,tuple) and len(valor) == 2)

    def interpolar(self, actor, atributo, valor):
        duracion = 0.5

        if isinstance(valor, tuple):
            duracion = valor[1]
            valor = valor[0]

        parametro = {atributo: valor[0]}

        tweener = self.pilas.obtener_escena_actual().tweener
        tweener.add_tween(actor, tween_time=duracion,
                          tween_type=tweener.IN_OUT_QUAD,
                          **parametro)

    def interpretar_propiedad_numerica(self, objeto, propiedad, valor):
        """Procesa una propiedad y permite que sea numero o interpolación.

        Este método se invoca en la mayoría de propiedades y atributos
        de actores en pilas-engine. Por ejemplo cuando se invoca a
        esta sentencia para mover al personaje:

            >>> actor.x = [100, 0, 200]

        o bien, para duplicar su tamaño en 10 segundos:

            >>> actor.escala = [2], 10
        """
        if isinstance(valor, int) or isinstance(valor, float):
            setattr(objeto, '_' + propiedad, valor)
        elif self.es_interpolacion(valor):
            self.interpolar(objeto, propiedad, valor)
        else:
            raise Exception("Solo se pueden asignar números o interpolaciones.")

    def interpolar_si_es_necesario(self, valor, nombre, tipo):
        # Si le indican dos argumentos, el primer sera
        # el valor de la interpolacion y el segundo la
        # velocidad.
        if isinstance(valor, tuple) and len(valor) == 2:
            duracion = valor[1]
            valor = valor[0]
        else:
            duracion = 1

        if isinstance(valor, list):
            valor = instanciar_interpolacion(self.pilas, valor, duracion=duracion, tipo=tipo)
        elif isinstance(valor, xrange):
            valor = instanciar_interpolacion(self.pilas, list(valor), duracion=duracion, tipo=tipo)

        if es_interpolacion(valor):
            valor.apply(valor, function=nombre)
        else:
            return valor


def obtener_ruta_al_recurso(ruta):
    dirs = ['./', '/../data',
            PATH,
            INTERPRETE_PATH,
            PATH + '/../',
            PATH + '/../data',
            INTERPRETE_PATH + '/data',
            PATH + '/../../data',
            INTERPRETE_PATH + '/../data'
           ]

    for x in dirs:
        full_path = os.path.join(x, ruta)

        if os.path.exists(full_path):
            return full_path

    # Si no ha encontrado el archivo lo reporta.
    raise IOError("El archivo '%s' no existe." % (ruta))

def instanciar_interpolacion(pilas, valor_o_valores, duracion=1, demora=0, tipo='lineal'):
    """Retorna un objeto que representa cambios de atributos progresivos.

    El resultado de esta función se puede aplicar a varios atributos
    de los actores, por ejemplo:

        >>> bomba = pilas.actores.Bomba()
        >>> bomba.escala = pilas.interpolar(3)

    Esta función también admite otros parámetros cómo:

    :param duracion: es la cantidad de segundos que demorará toda la interpolación.
    :param demora: cuantos segundos se deben esperar antes de iniciar.
    :param tipo: es el algoritmo de la interpolación, puede ser 'lineal'.
    """

    import interpolaciones

    algoritmos = {
        'lineal': interpolaciones.Lineal,
        'aceleracion_gradual': interpolaciones.AceleracionGradual,
        'desaceleracion_gradual': interpolaciones.DesaceleracionGradual,
        'rebote_inicial': interpolaciones.ReboteInicial,
        'rebote_final': interpolaciones.ReboteFinal,
        'elastico_inicial': interpolaciones.ElasticoInicial,
        'elastico_final': interpolaciones.ElasticoFinal
    }

    if tipo in algoritmos:
        clase = algoritmos[tipo]
    else:
        raise ValueError("El tipo de interpolacion %s es invalido" % (tipo))

    # Permite que los valores de interpolacion sean un numero o una lista.
    if not isinstance(valor_o_valores, list):
        valor_o_valores = [valor_o_valores]

    return clase(pilas, valor_o_valores, duracion, demora)


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


def verificar_si_lanas_existe(parent):
    import sys
    sys.path.append('../lanas')
    try:
        import lanas
    except ImportError:
        QtGui.QMessageBox.warning(parent, u"Error al inicializar pilas", u"No se puede encontrar el submódulo 'lanas'. \n\n¿Ejecutaste 'make actualizar' antes?")

