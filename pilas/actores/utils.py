# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import random
import pilas

def ordenar_actores_por_valor_z():
    "Ordena todos los actores para que se impriman con 'z' como criterio de orden."
    pilas.actores.todos.sort()

def insertar_como_nuevo_actor(actor):
    "Coloca a un actor en la lista de actores a imprimir en pantalla."
    pilas.actores.todos.append(actor)
    
def eliminar_un_actor(actor):
    try:
        pilas.actores.todos.remove(actor)
    except ValueError:
        #TODO: quitar este silenciador de excepcion.
        pass

def eliminar_a_todos():
    a_eliminar = list(pilas.actores.todos)
    a_eliminar = a_eliminar[1:]    # evita borrar el fondo.

    for x in a_eliminar:
        x.eliminar()

def destruir_a_todos():
    "Elimina a los actores inmediatamente (evita que exploten o hagan algo)."
    a_eliminar = list(pilas.actores.todos)

    for x in a_eliminar:
        x.destruir()

def obtener_actor_en(x, y):
    "Intenta obtener el actor mas cerca de la pantalla (z mas pequeño) en la posición (x, y)"

    # Busca el objeto que colisiones ordenando en sentido inverso.
    for sprite in pilas.actores.todos[::-1]:
        if sprite.colisiona_con_un_punto(x, y):
            return sprite

    return None


def fabricar(clase, cantidad=1, posiciones_al_azar=True, *k, **kv):
    "Genera muchas intancias de objetos asignando posiciones aleatorias."

    objetos_creados = []

    for x in range(cantidad):
        if posiciones_al_azar:
            x = random.randint(-300, 300)
            y = random.randint(-200, 200)
        else:
            x = 0
            y = 0

        kv['x'] = x
        kv['y'] = y
        nuevo = clase(*k, **kv)
        objetos_creados.append(nuevo)

    return pilas.grupo.Grupo(objetos_creados)
