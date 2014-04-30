# -*- encoding: utf-8 -*-


import time
import Image

from PyQt4 import QtGui
from pilas.fondos import *
from pilas.actores import Pizarra
from pilas.actores import Ejes
from datetime import datetime, timedelta

def _evaluarCuadrante(unActor):

    # Retorna la ubicación del actor teniendo en cuenta su rotación
    if (unActor.rotacion  >= 270 and unActor.rotacion < 360):    # Norte - noreste
        cuatri = 1
    elif (unActor.rotacion >= 0 and unActor.rotacion < 90):  # Este - sur
        cuatri = 2
    elif (unActor.rotacion >= 90 and unActor.rotacion < 180):  # Sur - oeste
        cuatri = 3
    else:
        cuatri = 4
    return cuatri
            

def _evaluarPerpendicularidadDeObjetos(robot, unactor, xRobotb, yRobotb, xActorb, yActorb) :

    distanciaEntreXactorX = xActorb - unactor.x
    distanciaEntreYactorY = yActorb - unactor.y

    distanciaEntreRobotA = xRobotb - robot.x
    distanciaEntreRobotB = yRobotb - robot.y

    # devuelve si las rectas son perpendiculares

    return ( (distanciaEntreXactorX * distanciaEntreRobotA) == 0) and ( (distanciaEntreYactorY * distanciaEntreRobotB) == 0 )


def _puntosParaLaRecta(unActor):

    # Retorna la ubicación del actor teniendo en cuenta su rotación
    # print "nActor.rotacion ", unActor.rotacion

    if (unActor.rotacion == 270):  # Norte
        # print " norte"
        puntoX = unActor.x
        puntoY = unActor.y + unActor.radio_de_colision

    elif ((unActor.rotacion > 270) and (unActor.rotacion < 360)): # norte- noreste
        # print "norte - este"
        puntoY = unActor.y + unActor.radio_de_colision
        puntoX = unActor.x +  unActor.radio_de_colision
    elif (unActor.rotacion == 0 ):  # Este
        # print "este"
        puntoX = unActor.x + unActor.radio_de_colision
        puntoY = unActor.y
    elif ((unActor.rotacion > 0) and (unActor.rotacion < 90)): #  Este - sur
        # print "este-sur"
        puntoY = unActor.y - unActor.radio_de_colision
        puntoX = unActor.x +  unActor.radio_de_colision
    elif (unActor.rotacion == 90):  # Sur
        # print "sur"
        puntoY = unActor.y -  unActor.radio_de_colision
        puntoX = unActor.x
    elif ((unActor.rotacion > 90)  and  (unActor.rotacion < 180 ) ):  # Sur - oeste
        # print "Sur - oeste"
        puntoY = unActor.y -  unActor.radio_de_colision
        puntoX = unActor.x -  unActor.radio_de_colision
    elif (unActor.rotacion == 180) : # Oeste
        # print "Oeste"
        puntoX = unActor.x -  unActor.radio_de_colision
        puntoY = unActor.y
    else:  
        # print " de 180 a 270"
        puntoY = unActor.y + unActor.radio_de_colision
        puntoX = unActor.x -  unActor.radio_de_colision
    

    return (puntoX, puntoY)

def _actor_no_valido(actor):
    return (not isinstance(actor, Pizarra) and (not isinstance(actor, Fondo)) and  (not isinstance(actor, Ejes)))
    
def wait(seconds = 0):
    """ Produce un retardo de seconds segundos en los que el robot no hace nada. """
 
    now = datetime.now()
    while now + timedelta(0, seconds, 0) > datetime.now():
        QtGui.QApplication.processEvents()



