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
    pilas.escena_actual().actores.sort()


def insertar_como_nuevo_actor(actor):
    """Coloca a un actor en la lista de actores a imprimir en pantalla.

    :param actor: Actor que se quiere comenzar a mostrar en pantalla.
    """
    pilas.escena_actual().actores.append(actor)
    actor.escena = pilas.escena_actual()


def eliminar_a_todos():
    """Elimina a todos los actores de la escena."""
    a_eliminar = pilas.escena_actual().actores[1:]  # evita borrar el fondo.

    for x in a_eliminar:
        x.eliminar()


def destruir_a_todos():
    """Elimina a los actores inmediatamente (evita que exploten o hagan algo)."""
    a_eliminar = pilas.escena_actual().actores[1:]  # evita borrar el fondo.

    for x in a_eliminar:
        x.destruir()


def obtener_actor_en(x, y):
    """Intenta obtener el actor mas cerca de la pantalla (z mas pequeño) en la posición (x, y)

    :param x: Posición horizontal del punto selección.
    :param y: Posición vertical del punto selección.
    """

    # Busca el objeto que colisiones ordenando en sentido inverso.
    for sprite in pilas.escena_actual().actores[::-1]:
        if sprite.colisiona_con_un_punto(x, y):
            return sprite

    return None


def fabricar(clase, cantidad=1, posiciones_al_azar=True, *k, **kv):
    """Genera muchas instancias de una clase particular asignando posiciones aleatorias.

        >>> pilas.utils.fabricar(pilas.actores.Caja, 30)

    :param clase: Clase del objeto a generar.
    :param cantidad: Cantidad de objetos que se van a crear de esa clase.
    :param posiciones_al_azar: True o False indicando si se tienen que dar posiciones al azar.
    """
    objetos_creados = []

    for x in range(cantidad):
        if posiciones_al_azar:
            ancho, alto = pilas.mundo.obtener_area()
            mitad_ancho = ancho/2
            mitad_alto = alto/2
            x = random.randint(-mitad_ancho, mitad_ancho)
            y = random.randint(-mitad_alto, mitad_alto)
        else:
            x = 0
            y = 0

        kv['x'] = x
        kv['y'] = y
        nuevo = clase(*k, **kv)
        objetos_creados.append(nuevo)

    return pilas.grupo.Grupo(objetos_creados)
