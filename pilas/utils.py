# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
import interpolaciones
import sys
import subprocess
import math
import uuid

import pilas


PATH = os.path.dirname(os.path.abspath(__file__))


def es_interpolacion(an_object):
    "Indica si un objeto se comporta como una colisión."

    return isinstance(an_object, interpolaciones.Interpolacion)


def obtener_ruta_al_recurso(ruta):
    """Busca la ruta a un archivo de recursos.

    Los archivos de recursos (como las imagenes) se buscan en varios
    directorios (ver docstring de image.load), así que esta
    función intentará dar con el archivo en cuestión.
    """

    dirs = ['./', os.path.dirname(sys.argv[0]), 'data', PATH, PATH + '/data']


    for x in dirs:
        full_path = os.path.join(x, ruta)
        #DEBUG: print "buscando en: '%s'" %(full_path)

        if os.path.exists(full_path):
            return full_path

    # Si no ha encontrado el archivo lo reporta.
    raise IOError("El archivo '%s' no existe." %(ruta))


def esta_en_sesion_interactiva():
    "Indica si pilas se ha ejecutado desde una consola interactiva de python."
    import sys
    try:
        cursor = sys.ps1
        return True
    except AttributeError:
        try:
            in_ipython = sys.ipcompleter
            return True
        except AttributeError:
            if sys.stdin.__class__.__module__.startswith("idle"):
                return True

    return False

def distancia(a, b):
    "Retorna la distancia entre dos numeros."
    return abs(b - a)

def distancia_entre_dos_puntos((x1, y1), (x2, y2)):
    "Retorna la distancia entre dos puntos en dos dimensiones."
    return math.sqrt(distancia(x1, x2) ** 2 + distancia(y1, y2) ** 2)

def distancia_entre_dos_actores(a, b):
    return distancia_entre_dos_puntos((a.x, a.y), (b.x, b.y))

def colisionan(a, b):
    "Retorna True si dos actores estan en contacto."
    return distancia_entre_dos_actores(a, b) < a.radio_de_colision + b.radio_de_colision

def interpolable(f):
    "Decorador que se aplica a un metodo para que permita animaciones de interpolaciones."

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
            value = interpolar(value, duracion=duracion)
        elif isinstance(value, xrange):
            value = interpolar(list(value), duracion=duracion)

        if es_interpolacion(value):
            value.apply(args[0], function=f.__name__)
        else:
            f(args[0], value, **kwargs)

    return inner

def hacer_coordenada_mundo(x, y):
    dx, dy = pilas.mundo.motor.centro_fisico()
    return (x + dx, dy - y)

def hacer_coordenada_pantalla_absoluta(x, y):
    dx, dy = pilas.mundo.motor.centro_fisico()
    return (x + dx, dy - y)

def listar_actores_en_consola():
    todos = pilas.escena_actual().actores

    print "Hay %d actores en la escena:" %(len(todos))
    print ""

    for s in todos:
        print "\t", s

    print ""

def obtener_angulo_entre(punto_a, punto_b):
    (x, y) = punto_a
    (x1, y1) = punto_b
    return math.degrees(math.atan2(y1 - y, x1 -x))

def convertir_de_posicion_relativa_a_fisica(x, y):
    dx, dy = pilas.mundo.motor.centro_fisico()
    return (x + dx, dy - y)

def convertir_de_posicion_fisica_relativa(x, y):
    dx, dy = pilas.mundo.motor.centro_fisico()
    return (x - dx, dy - y)

def interpolar(valor_o_valores, duracion=1, demora=0, tipo='lineal'):
    """Retorna un objeto que representa cambios de atributos progresivos.

    El resultado de esta función se puede aplicar a varios atributos
    de los actores, por ejemplo::

        bomba = pilas.actores.Bomba()
        bomba.escala = pilas.interpolar(3)

    Esta función también admite otros parámetros cómo:

        - duracion: es la cantidad de segundos que demorará toda la interpolación.
        - demora: cuantos segundos se deben esperar antes de iniciar.
        - tipo: es el algoritmo de la interpolación, puede ser 'lineal'.
    """


    import interpolaciones

    algoritmos = {
            'lineal': interpolaciones.Lineal,
            }

    if algoritmos.has_key('lineal'):
        clase = algoritmos[tipo]
    else:
        raise ValueError("El tipo de interpolacion %s es invalido" %(tipo))

    # Permite que los valores de interpolacion sean un numero o una lista.
    if not isinstance(valor_o_valores, list):
        valor_o_valores = [valor_o_valores]

    return clase(valor_o_valores, duracion, demora)

def obtener_area():
    "Retorna el area que ocupa la ventana"
    return pilas.mundo.motor.obtener_area()

def obtener_bordes():
    ancho, alto = pilas.mundo.motor.obtener_area()
    return -ancho/2, ancho/2, alto/2, -alto/2

def obtener_area_de_texto(texto):
    "Informa el ancho y alto que necesitara un texto para imprimirse."
    return pilas.mundo.motor.obtener_area_de_texto(texto)

def realizar_pruebas():
    print "Realizando pruebas de dependencias:"
    print ""

    print "Box 2D:",

    if pilas.fisica.obtener_version().startswith("2.1"):
        print "OK, versión", pilas.fisica.obtener_version()
    else:
        print "Error -> la versión está obsoleta, instale una versión de la serie 2.1"

    print "pyqt:",

    try:
        from PyQt4 import Qt
        print "OK, versión", Qt.PYQT_VERSION_STR
    except ImportError:
        print "Error -> no se encuentra pyqt."

    print "pyqt con aceleracion:",

    try:
        from PyQt4 import QtOpenGL
        from PyQt4.QtOpenGL import QGLWidget
        print "OK"
    except ImportError:
        print "Error -> no se encuentra pyqt4gl."

    print "PIL para soporte de jpeg (opcional):",

    try:
        from PIL import Image
        print "OK"
    except ImportError:
        print "Cuidado -> no se encuentra PIL."

def ver_codigo(objeto, imprimir, retornar):
    """Imprime en pantalla el codigo fuente asociado a un objeto."""
    import inspect

    try:
        codigo = inspect.getsource(objeto.__class__)
    except TypeError:
        codigo = inspect.getsource(objeto)

    if imprimir:
        print codigo

    if retornar:
        return codigo

def obtener_uuid():
    return str(uuid.uuid4())

def abrir_archivo_con_aplicacion_predeterminada(ruta_al_archivo):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', ruta_al_archivo))
    elif os.name == 'nt':
        os.startfile(ruta_al_archivo)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', ruta_al_archivo))

def centrar_ventana(widget):
    from PyQt4 import QtGui
    desktop = QtGui.QApplication.desktop()
    widget.move(desktop.screen().rect().center() - widget.rect().center())

def descargar_archivo_desde_internet(parent, url, archivo_destino):
    import descargar
    ventana = descargar.Descargar(parent, url, archivo_destino)
    ventana.show()

def imprimir_todos_los_eventos():
    "Muestra en consola los eventos activos y a quienes invocan"
    import pilas

    for x in dir(pilas.escena_actual()):
        attributo = getattr(pilas.escena_actual(), x)

        if isinstance(attributo, pilas.evento.Evento):
            print "Evento:", attributo.nombre
            attributo.imprimir_funciones_conectadas()
            print ""
