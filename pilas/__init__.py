# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import simbolos
import os
import sys
import time

import colores
import actores
import imagenes
import sonidos
import utils
from interpolaciones import Lineal
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
import random
import ejemplos
import inspect
import red
import motores


# Inicialmente comienza sin un mundo esperando a que se inicialice.
mundo = None
motor = motores.pySFML()
bg = None
colisiones = Colisiones()

def iniciar(ancho=640, alto=480, titulo='Pilas'):
    global mundo

    # Cuando inicia en modo interactivo se asegura
    # de crear la ventana dentro del mismo hilo que
    # tiene el contexto opengl.
    if utils.esta_en_sesion_interactiva():
        pilas.utils.cargar_autocompletado()
        iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo + " [Modo Interactivo]")
    else:
        mundo = Mundo(ancho, alto, titulo)
        escenas.Normal()

def terminar():
    global mundo
    mundo.terminar()

def ejecutar():
    "Pone en funcionamiento el ejecutar principal."
    global mundo

    if mundo:
        mundo.ejecutar_bucle_principal()
    else:
        raise Exception("Tienes que llamar a pilas.iniciar() antes de ejecutar el juego.")

def iniciar_y_ejecutar(ancho, alto, titulo):
    global mundo

    mundo = Mundo(ancho, alto, titulo)
    escenas.Normal()
    ejecutar()


def iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo):
    "Ejecuta el bucle de pilas en segundo plano."
    import threading
    global gb

    bg = threading.Thread(target=iniciar_y_ejecutar, args=(ancho, alto, titulo))
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
            'lineal': Lineal,
            }

    if algoritmos.has_key('lineal'):
        clase = algoritmos[tipo]
    else:
        raise ValueError("El tipo de interpolacion %s es invalido" %(tipo))

    # Permite que los valores de interpolacion sean un numero o una lista.
    if not isinstance(valor_o_valores, list):
        valor_o_valores = [valor_o_valores]

    return clase(valor_o_valores, duracion, demora)


def ver(objeto):
    "Imprime en pantalla el codigo fuente asociado a un objeto o elemento de pilas."

    if isinstance(objeto, object):
        codigo = inspect.getsource(objeto.__class__)
    else:
        codigo = inspect.getsource(objeto)

    print codigo


def avisar(mensaje):
    "Emite un mensaje en la ventana principal."
    texto = actores.Texto(mensaje)
    texto.magnitud = 22
    texto.izquierda = -310
    texto.abajo = -230


def fabricar(clase, cantidad=1):
    "Genera muchas intancias de objetos asignando posiciones aleatorias."

    objetos_creados = []

    for x in range(cantidad):
        x = random.randint(-300, 300)
        y = random.randint(-200, 200)

        nuevo = clase()
        nuevo.x = x
        nuevo.y = y
        objetos_creados.append(nuevo)

    return objetos_creados
