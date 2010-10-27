# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

mundo = None
motor = None
bg = None

def iniciar(ancho=640, alto=480, titulo='Pilas', usar_motor='pysfml'):
    global mundo
    global motor

    import motores

    motores_disponibles = {
            'pysfml': motores.pySFML,
            'sfml': motores.pySFML,
            'pygame': motores.Pygame,
    }

    motor = motores_disponibles[usar_motor]()

    import simbolos
    import os
    import sys
    import time

    import base
    import colores
    import imagenes
    import sonidos
    import actores
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


    pilas.colisiones = Colisiones()



    # Cuando inicia en modo interactivo se asegura
    # de crear la ventana dentro del mismo hilo que
    # tiene el contexto opengl.
    if utils.esta_en_sesion_interactiva():
        pilas.utils.cargar_autocompletado()
        iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo + " [Modo Interactivo]")
    else:
        mundo = pilas.mundo.Mundo(ancho, alto, titulo)
        escenas.Normal()

def terminar():
    global mundo

    if mundo:
        mundo.terminar()
    else:
        print "No se puede terminar pilas porque no la has inicializado."

def ejecutar():
    "Pone en funcionamiento el ejecutar principal."
    global mundo

    if mundo:
        mundo.ejecutar_bucle_principal()
    else:
        raise Exception("Tienes que llamar a pilas.iniciar() antes de ejecutar el juego.")

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
