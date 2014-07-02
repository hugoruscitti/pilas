# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
import sys
import uuid
import math

from pilasengine import colores
import pitweener

from PyQt4 import QtGui

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
INTERPRETE_PATH = os.path.dirname(sys.argv[0])

# Relación de pixels por metro (para el motor de física).
PPM = 30


class Utils(object):

    def __init__(self, pilas):
        self.pilas = pilas

    def obtener_uuid(self):
        """Genera un identificador único."""
        return str(uuid.uuid4())

    def obtener_area_de_texto(self, cadena, magnitud=10, vertical=False,
                              fuente=None, ancho=0):
        texto = self.pilas.imagenes.crear_texto(cadena, magnitud, vertical,
                                                fuente, colores.blanco, ancho)
        return (texto.ancho(), texto.alto())

    def es_interpolacion(self, valor):
        return isinstance(valor, list) or (isinstance(valor, tuple) and
                                           len(valor) == 2)

    def interpolar(self, actor, atributo, valor):
        duracion = 0.5

        if isinstance(valor, tuple):
            duracion = valor[1]
            valor = valor[0]

        tweener = self.pilas.obtener_escena_actual().tweener
        anterior = None

        for (i, x) in enumerate(valor):
            demora_inicial = i * duracion
            parametro = {atributo: x}
            tweener.add_tween(actor, tween_time=duracion,
                              tween_type=tweener.IN_OUT_QUAD,
                              tween_delay=demora_inicial,
                              inicial=anterior,
                              **parametro)
            anterior = x

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


def obtener_angulo_entre(punto_a, punto_b):
    """Retorna el ángulo entro dos puntos de la pantalla.

    :param punto_a: Una tupla con la coordenada del primer punto.
    :param punto_b: Una tupla con la coordenada del segundo punto.
    """
    (x, y) = punto_a
    (x1, y1) = punto_b
    return math.degrees(math.atan2(y1 - y, x1 - x))


def convertir_a_metros(valor):
    """Convierte una magnitid de pixels a metros."""
    return valor / float(PPM)


def convertir_a_pixels(valor):
    """Convierte una magnitud de metros a pixels."""
    return valor * PPM


def obtener_ruta_al_recurso(ruta):
    dirs = ['./', '/../data',
            PATH,
            INTERPRETE_PATH,
            PATH + '/data/',
            INTERPRETE_PATH + '/data/',
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


def instanciar_interpolacion(pilas, valor_o_valores, duracion=1, demora=0,
                             tipo='lineal'):
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


def centrar_ventana(ventana):
    """Mueve la ventana al centro del area visible del escritorio."""
    qr = ventana.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    ventana.move(qr.topLeft())

def realizar_pruebas():
    """Imprime pruebas en pantalla para detectar si pilas tiene todas las dependencias instaladas."""

    n='[0m'
    v='[01;32m'

    print "Realizando pruebas de dependencias:"
    print ""

    print "Box 2D:",

    try:
        import Box2D as box2d

        ver = box2d.__version_info__

        if ver[0] == 2 and ver[1] >= 1:
            print v+"OK, versión " + str(box2d.__version__) + n
        else:
            print "Error -> la versión está obsoleta, instale una versión de la serie 2.1, 2.2 o 2.3"
    except ImportError:
        print "Error -> no se encuentra pybox2d"

    print "pyqt:",

    try:
        from PyQt4 import Qt
        print v+"OK, versión "+Qt.PYQT_VERSION_STR+n
    except ImportError:
        print "Error -> no se encuentra pyqt."

    print "pyqt con aceleracion:",

    try:
        from PyQt4 import QtOpenGL
        from PyQt4.QtOpenGL import QGLWidget
        print v+"OK"+n
    except ImportError:
        print "Error -> no se encuentra pyqt4gl."

    print "PIL para soporte de jpeg (opcional):",

    try:
        from PIL import Image
        print v+"OK"+n
    except ImportError:
        print "Cuidado -> no se encuentra PIL."

    print "pygame:",

    try:
        import pygame
        print v+"OK"+n
    except ImportError:
        print "Cuidado -> no se encuentra pygame."
