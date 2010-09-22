# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import os
import sys
import time

from PySFML import sf

import actores
import imagenes
import sonidos
import utils
import interpolaciones
import dispatch
import eventos
import habilidades
import ventana
import comportamientos
import escenas
from control import Control
from camara import Camara
import copy
import pilas.utils
from mundo import Mundo
from colisiones import Colisiones


# Inicialmente comienza sin un mundo esperando a que se inicialice.
mundo = None
colisiones = Colisiones()

def iniciar(ancho=640, alto=480, titulo='Pilas'):
    global mundo
    mundo = Mundo(ancho, alto, titulo)
    escenas.Normal()

def terminar():
    global mundo
    mundo.terminar()

def ejecutar():
    "Pone en funcionamiento el ejecutar principal."
    global mundo

    if not mundo:
        iniciar()

    mundo.ejecutar_bucle_principal()


def ejecutar_en_segundo_plano():
    "Ejecuta el ejecutar de pilas en segundo plano."
    import threading

    bg = threading.Thread(target=ejecutar)
    bg.start()


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


def avisar(mensaje):
    "Emite un mensaje en la ventana principal."
    texto = actores.Texto(mensaje)
    texto.magnitud = 22
    texto.izquierda = -320
    texto.abajo = -240


# Cuando inicia en modo interactivo se asegura
# de crear la ventana dentro del mismo hilo que
# tiene el contexto opengl.
if utils.esta_en_sesion_interactiva():
    pilas.utils.cargar_autocompletado()
    ejecutar_en_segundo_plano()
else:
    pass
