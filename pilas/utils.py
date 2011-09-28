# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import os
import shutil
import interpolaciones
import sys
import subprocess
import math

import pilas
import xmlreader


PATH = os.path.dirname(os.path.abspath(__file__))


def cargar_autocompletado():
    "Carga los modulos de python para autocompletar desde la consola interactiva."
    try:
        import rlcompleter
        import readline

        readline.parse_and_bind("tab: complete")
    except ImportError:
        print "No se puede cargar el autocompletado, instale readline..."

def hacer_flotante_la_ventana():
    "Hace flotante la ventana para i3 (el manejador de ventanas que utiliza hugo...)"
    try:
        subprocess.call(['i3-msg', 't'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        pass

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

def crear_juego():
    nombre = raw_input("Indica el nombre del juego: ")
    shutil.copytree(PATH + "/data/juegobase", nombre)

    print "Se ha creado el directorio '%s'" %(nombre)
    print "Ingresa en el directorio y econtrarás los archivos iniciales del juego."


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
    todos = pilas.actores.todos
    
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

    try:
        import Box2D as box2d
        print "OK, versión", box2d.__version__
    except ImportError:
        print "Error -> no se encuentra pybox2d."

    print "pygame:",

    try:
        import pygame
        print "OK, versión", pygame.__version__
    except ImportError:
        print "Error -> no se encuentra pygame."

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
