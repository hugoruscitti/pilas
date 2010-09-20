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

def iniciar():
    global mundo
    mundo = Mundo()
    escenas.Normal()


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


def interpolar(*values, **kv):
    "Retorna un objeto de interlacion que se puede asignar a una propiedad."

    if 'duracion' in kv:
        duration = kv.pop('duracion')
    else:
        duration = 5

    if 'demora' in kv:
        delay = kv.pop('demora')
    else:
        delay = 0

    if 'tipo' in kv:
        tipo = kv.pop('tipo')
    else:
        tipo = 'lineal'

    if tipo == 'lineal':
        clase = interpolaciones.Lineal
    else:
        raise ValueError("El tipo de interpolacion %s es invalido" %(tipo))

    return clase(values, duration, delay)


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
