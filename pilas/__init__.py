# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


"""
Pilas engine - Un motor para realizar videojuegos.
==================================================

Este es el módulo principal de pilas. Desde aquí
puedes acceder a toda la funcionalidad del motor.

"""
import os
import sys
import time

from PySFML import sf

import actores
import imagenes
import sonidos
import tareas
import pytweener
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


# Inicialmente comienza sin un mundo esperando a que se inicialice.
mundo = None



tweener = pytweener.Tweener()

event = 1
clock = 1
control = 1
camara = 1
escena = 0

path = os.path.dirname(os.path.abspath(__file__))
tasks = tareas.Tareas() 
 
def agregar_tarea(time_out, function, *params): 
    tasks.agregar(time_out, function, params)


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

def ordenar_actores_por_valor_z():
    "Define el orden de impresion en pantalla."
    actores.todos.sort()


def avisar(mensaje):
    texto = actores.Texto(mensaje)
    texto.magnitud = 22
    texto.izquierda = -320
    texto.abajo = -240

def definir_escena(escena_nueva):
    "Cambia la escena actual y elimina a todos los actores de la pantalla."
    global mundo
    mundo.definir_escena(escena_nueva)


# Detecta si la biblioteca se esta ejecutando
# desde el modo interactivo o desde un script.

# Cuando inicia en modo interactivo se asegura
# de crear la ventana dentro del mismo hilo que
# tiene el contexto opengl.

if utils.esta_en_sesion_interactiva():
    pilas.utils.cargar_autocompletado()
    ejecutar_en_segundo_plano()
else:
    pass
