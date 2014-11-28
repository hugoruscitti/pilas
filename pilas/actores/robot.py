# -*- encoding: utf-8 -*-

import pilas
import time
import sys
import math
import pygame
import numpy
import Image
import weakref

from PyQt4 import QtGui, uic

from datetime import datetime, timedelta

from pilas.actores import Actor
from pilas.fondos import  *
from pilas.actores import Pizarra
from pilas.actores import Nave
import pilas.utils as utils
from pilas.fondos import *
from pilas.actores import Ejes

# Calculos para sensor Ping

EPSILON = 0.0001

def _puntos_de_la_linea(x1, y1, x2, y2):
    float(x1)
    float(x2)
    float(y1)
    float(y2)
    
    # x2, y2 = _puntosParaLaRecta(unActor) # punto y pendiente
    linea = {}
    if (x1 == x2):
        linea["A"] = 1
        linea["B"] = 0
        # linea["c"] = 1  unActor.x * (-1)
        linea["C"] = x1 * (-1)
    else:
        linea["B"] = 1
        linea["A"] =  (-1 * (y1 - y2))   / (x1 - x2)
        linea["C"] =  ( -1 * (linea ["A"] * x1)) - (linea["B"] * y1)
    
    return linea

def _puntoEInterseccionConLaLinea(puntoX, puntoY, pendienteM ):

    linea = {}
    linea["A"] = pendienteM * -1
    linea["B"] = 1
    linea["C"]  = ( (linea["A"] * puntoX)  + (linea["B"] * puntoY) ) * -1
    return linea

def _sonParalelas(linea1, linea2):
    
    return ((math.fabs(linea1["A"] - linea2["A"]) <= EPSILON ) and (math.fabs(linea1["B"] - linea2["B"]) <= EPSILON ))

def _sonCoincidentes(linea1, linea2):
   
    return(( _sonParalelas(linea1, linea2))  and ( math.fabs(linea1["C"] - linea2["C"]) <= EPSILON ))

def _interseccionEntreLineas(linea1, linea2):
    
    if  (_sonCoincidentes(linea1, linea2)):
        return (0,0)
    if (_sonParalelas(linea1, linea2)):
        return None

    px = ((linea2["B"] * linea1["C"] ) - (linea1["B"] * linea2["C"])) / ( (linea2["A"] * linea1["B"] ) - (linea2["B"] * linea1["A"] )   )


    if math.fabs(linea1["B"] > EPSILON): #lineas verticales
        py =  -1 * ( linea1["A"] * px + linea1["C"] ) / linea1["B"]
    else:
        py = -1 * (linea2["A"]  * px + linea2["C"] ) / linea2["B"]
        
    return (px, py)		

def _verificarPuntoEnLaCircunferencia(x1, y1, x2, y2, radio):
    
    # Ingresan centro de actor y pnto de interseccion
    float(x1)
    float(y1)
    float(x2)
    float(y2)
    
    dis  = utils.distancia_entre_dos_puntos((x1, y1), (x2, y2)) 
  
    return dis <= radio


def _actorDetrasDelRobot(psX, psY, crX, crY, piX, piY):
    segSenCentroX = psX - crX
    segSenCentroY = psY - crY

    segIntCentroX = piX -  crX
    segIntCentroY = piY -  crY

    if (segSenCentroX * segSenCentroY  <  0):# Las X son de distinto signo
        return False
    else:
        return True
    

def _actor_no_valido(actor):
    return (not isinstance(actor, Pizarra) and (not isinstance(actor, Fondo)) and  (not isinstance(actor, Ejes))  )

def wait(seconds = 0):
    """ Produce un retardo de seconds segundos en los que el robot no hace nada. """

    now = datetime.now()
    while now + timedelta(0, seconds, 0) > datetime.now():
        QtGui.QApplication.processEvents()


def _puntosParaLaRecta(x, y, grados, distancia):
    
    # Retorna otro punto para la recta, teniendo en cuenta su rotación

    radianes = math.radians(360 - grados)
    
    puntoX = math.cos(radianes) * distancia + x
    puntoY = math.sin(radianes) * distancia + y

    return (puntoX, puntoY)

#### Robot

class Robot(object):


                        
    def __init__(self,board, robotid=0, x=0, y=0):
        """ Inicializa el robot y lo asocia con la placa board. """

        self.actor = pilas.actores.Tortuga()
        imagen = pilas.imagenes.cargar('RobotN6.png')
        self.actor.set_imagen(imagen)
        self.actor.rotacion = 270
        self.actor.velocidad = 3
        self.actor.pasos = 1
        self.actor.anterior_x = x
        self.actor.anterior_y = y
        self.actor.bajalapiz()
        self.actor.bajalapiz()
        self.actor.radio_de_colision = 31
        self.actor.color = pilas.colores.negro
        
        
        # Se queda en pantalla
        self.actor.aprender(pilas.habilidades.SeMantieneEnPantalla)
        # Se puede arrastrar con el mouse
        self.actor.aprender(pilas.habilidades.Arrastrable)

        self.radio_de_colision = self.actor.radio_de_colision
        self.robotid = robotid
        self.board = board
        self.name = ''
        self.proxy = weakref.proxy(self)
        self.board.agregarRobot(self.proxy)
        self.tarea = None


    def __getattribute__(self, metodo):
        atributos = ["forward", "backward", "turnLeft", "turnRight", "beep", 
                        "getObstacle","getLine", "ping", "stop", "battery" , "senses",
                        "setId", "setName" , "getName", "speak", "bajalapiz" , "subelapiz",
                        "set_x", "set_y", "get_x", "get_y" ]
        if metodo in atributos:
            QtGui.QApplication.processEvents()

        return object.__getattribute__(self, metodo)
             

    # Redefinir el método eliminar de la clase Actor para que lo elimine también de la lista de robots de Board
    def eliminar(self):
        self.board.eliminarDeLaLista(self.proxy)
        self.actor.eliminar()

    ## Movimiento horizontal y vertical

    def _setVelocidad(self, valor):
        """ Asigna una velocidad de movimiento real al robot """
        if ((valor % 2 == 0) and (valor % 10 == 0)):
            self.actor.velocidad = valor / 10 / 2
        else:
            cvalor = valor / 10
            self.actor.velocidad = (cvalor / 2 ) + 1

    def _velocidadValida(self, vel, exta, extb):
        return ((vel >= exta) & (vel <= extb))

    def forward(self, vel=50, seconds=-1):
        """ El robot avanza con velocidad vel durante seconds segundos. """
        self.stop()
        self.board._mover(self, vel,  seconds)
        QtGui.QApplication.processEvents()


    def _realizarMovimiento(self, vel, seconds):
        """ El robot avanza con velocidad vel durante seconds segundos. """

        def adelanteSinTiempo():
            self.actor.hacer(pilas.comportamientos.Avanzar(self.actor.velocidad, self.actor.velocidad))
            return (self.movimiento)

        def atrasSinTiempo():
            self.actor.hacer(pilas.comportamientos.Retroceder(self.actor.velocidad, self.actor.velocidad))
            return (self.movimiento)

        self.stop()
        self._setVelocidad(vel)

        if (self._velocidadValida(vel, 10, 100)) :
            self.movimiento = True
            self.tarea = pilas.escena_actual().tareas.condicional(0.1, adelanteSinTiempo)
            if (seconds != -1):
                wait(seconds)
                self.stop()
        elif (self._velocidadValida(vel, -100, -10)) :
            self.movimiento = True
            self.tarea = pilas.escena_actual().tareas.condicional(0.1, atrasSinTiempo)
            self.actor.velocidad = self.actor.velocidad * -1
            if (seconds != -1):
                wait(seconds)
                self.stop()
        else:
            print   """ Rangos de velocidades válidas:
                                -100 a -10
                                  10 a 100   """


    def backward(self, vel=50, seconds=-1):
        """ El robot retrocede con velocidad vel durante seconds segundos.  """
        self.stop()
        self.board._mover(self, -vel, seconds)

    ## Movimiento de giro
    def turnRight(self, vel=50, seconds=-1):
        """ El robot gira a la derecha con velocidad vel durante seconds segundos. """
        self.stop()
        self.board._girar(self, vel, seconds)

    def _realizarGiro(self, vel, seconds):

        def izquierdaSinTiempo():
            self.actor.hacer(pilas.comportamientos.Girar(-abs(self.actor.velocidad), self.actor.velocidad))
            return (self.movimiento)

        def derechaSinTiempo():
            self.actor.hacer(pilas.comportamientos.Girar(abs(self.actor.velocidad), self.actor.velocidad))
            return (self.movimiento)

        self.stop()
        self._setVelocidad(vel)


        if (self._velocidadValida(vel, 10, 100)) :
            self.movimiento = True
            self.tarea = pilas.escena_actual().tareas.condicional(0.1, derechaSinTiempo)
            if (seconds != -1):
                wait(seconds)
                self.stop()
        elif (self._velocidadValida(vel, -100, -10)) :
            self.movimiento = True
            self.tarea = pilas.escena_actual().tareas.condicional(0.1, izquierdaSinTiempo)
            self.actor.velocidad = self.actor.velocidad * -1
            if (seconds != -1):
                 wait(seconds)
                 self.stop()
        else:
            print   """ Rangos de velocidades válidas:
                                -100 a -10
                                  10 a 100   """


    def turnLeft(self, vel=50, seconds=-1):
        """ El robot gira a la izquierda con velocidad vel durante seconds segundos. """
        self.stop()
        self.board._girar(self, -vel, seconds)


    def beep(self, freq = 200, seconds=0):
        """ Hace que el robot emita un pitido con frecuencia freq durante seconds segundos."""
        utils.beep(freq, seconds)

    def _detenerse(self):
        self.movimiento = False
        if not (self.tarea is None):
            self.tarea.terminar()
        self.tarea = None

    def stop(self):
        self.board._detener(self)

    def battery(self):
        """ Devuelve el voltaje de las baterías del robot. """
        return 0


    def getObstacle(self, distance=100):
        """ Devuelve True si hay un obstaculo a menos de distance
        centimetros del robot. """
        valor =  self.ping()
        if (valor <= distance):
			
            return True
        else:
            return False

    def ping(self):
        """ Devuelve la distancia en centimetros al objeto frente al robot. """

        actoresValidos = self._actoresEnLaEscena()
        
        x2, y2 = _puntosParaLaRecta(self.actor.x, self.actor.y, self.actor.rotacion, 200)
        
        linea_actor_1 = _puntos_de_la_linea(self.actor.x, self.actor.y, x2, y2)
        

        if linea_actor_1["B"] == 0:
            pendiente = 0
        elif abs(linea_actor_1["A"]) > EPSILON:
            pendiente = 1.0 / linea_actor_1["A"] 
      
        valor = 601
        
        for otroActor in actoresValidos :
            if abs(linea_actor_1["A"]) > EPSILON:
                linea_generada =  _puntoEInterseccionConLaLinea(otroActor.x, otroActor.y, pendiente)
            else:
                linea_generada = {
                    "A": 1,
                    "B": 0,
                    "C": -otroActor.x
                }

            if _interseccionEntreLineas(linea_actor_1, linea_generada) is None:
                continue

            # No son paralelas
            oax2, oay2 = _interseccionEntreLineas(linea_actor_1, linea_generada)
            
            # Si está atrás del robot
            if self._esta_atras(x2, y2, oax2, oay2):
                continue
                           
            # Si la intersección está fuera de la circ. del actor no hay obstáculo
            if not _verificarPuntoEnLaCircunferencia(otroActor.x, otroActor.y, oax2, oay2, otroActor.radio_de_colision):
                continue

            # las rectas son perpendiculares y el punto en comun está en el area del otroActor
            # Calcular la distancia entre el actor y el punto de interseccion con el actor
            valorActual = utils.distancia_entre_dos_actores(self.actor, otroActor)
            if (valorActual < valor):
                valor = valorActual  
        

        return valor 
    
    def _esta_atras(self, p1x, p1y, p2x, p2y):
        d1x = p1x - self.actor.x
        d1y = p1y - self.actor.y
        d2x = p2x - self.actor.x
        d2y = p2y - self.actor.y
        
        return d1x * d2x < 0 or d1y * d2y < 0
        

    def getLine(self):
        """ Devuelve los valores de los sensores de linea. """

        ancho, alto =  pilas.mundo.gestor_escenas.escena_actual().get_fondo().dimension_fondo()

        xb, yb =  _puntosParaLaRecta(self.actor.x, self.actor.y, self.actor.rotacion, 31)

        vi = 0
        ximagen = ancho / 2 + xb
        yimagen = alto / 2 - yb
        valores = pilas.mundo.gestor_escenas.escena_actual().get_fondo().informacion_de_un_pixel(ximagen, yimagen)
        for i in valores:
            vi = vi + i

        return (vi / 3.0 , vi / 3.0)

    def senses(self):
        ventana = Sense(self)

    ## Identificadores

    def setId(self, newid):
        """  Setea el robotid  """
        self.robotid = newid

    def setName(self, name):
        """ Setea el nombre para el robot. """
        self.name = str(name)

    def getId(self):
        """  Devuelve el robotid. """
        return self.robotid

    def getName(self):
        """ Devuelve el nombre del robot. """
        return self.name

    ## Otras funciones

    def speak(self, msj):
        """ Imprime en la terminal el mensaje msj. """
        print msj

    def __del__(self):
        self.eliminar()

    def bajalapiz(self):
        """Le indica al robot si debe comenzar a dibujar con cada movimiento."""
        self.actor.lapiz_bajo = True

    def subelapiz(self):
        """Le indica al robot que deje de dibujar con cada movimiento."""
        self.actor.lapiz_bajo = False
        
    # Posicionamiento
        
    def set_x(self, valor):
        self.actor.x = valor
    
    def get_x(self):
        return self.actor.x
        
    def set_y(self, valor):
        self.actor.x = valor
        
    def get_y(self):
        return self.actor.y
        
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    
    
    def _actoresEnLaEscena(self):
        actores = []
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self.actor) and _actor_no_valido(actor)   ):
                actores.append(actor)
        return actores
    
class Board(object):

    def __init__(self, device='/dev/ttyUSB0'):
        """Inicializa el dispositivo de conexion con el/los robot/s  """
        self.device = device
        self.listaDeRobots = []

    #  Agrega un robot a la lista de reobots de un determinado Board
    # Decidir qué hacer cuando se agrega la misma variable con Id de robot diferente
    def agregarRobot(self, unRobot):
        self.listaDeRobots.append(unRobot)

    # Eliminar un robot de la lista de robots de un determinado Board
    def eliminarDeLaLista(self, unRobot):
        self.listaDeRobots.remove(unRobot)

    def boards(self):
        return self.device


    def _eliminarRobots(self):
        for i in self.listaDeRobots:
            del(i)

    def exit(self):
        self._eliminarRobots()
        del(self)

    def report(self):
        """ Retorna los números de ID's de los robots creados en el intérprete  """
        for i in self.listaDeRobots:
            print i.getId()

    def _mover(self,unRobot, vel, seconds):
        """ Envía un movimiento  vertical/horizontal a toos los robots con el mismo ID  """ 
        for i in self.listaDeRobots:
            if (i.getId() == unRobot.getId()) :
                i._realizarMovimiento(vel, seconds)

    def _girar(self,unRobot, vel, seconds):
        """ Envía un movimiento a izquierda/derecha a toos los robots con el mismo ID  """
        for i in self.listaDeRobots:
            if (i.getId() == unRobot.getId()) :
                i._realizarGiro(vel, seconds)

    def _detener(self, unRobot):
        for i in self.listaDeRobots:
            if (i.getId() == unRobot.getId()) :
                i._detenerse()


        
class Sense(QtGui.QMainWindow):
    def __init__(self, unRobot):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("/usr/local/lib/python2.7/dist-packages/pilas-0.81-py2.7.egg/pilas/data/senses.ui")
        self.activo = True
        self._mostrarInfo(unRobot)
        self.ui.show()

    #Definición de un evento para la salida del programa
    def closeEvent(self, event):
        self.activo = False
        event.accept()

    def _mostrarInfo(self, unRobot):

        def mostrarBateria():
            self.ui.battery.display(  '%0.2f' %  unRobot.battery())
            return self.activo

        def mostrarPing():
            self.ui.nping.display(  '%0.2f' %  unRobot.ping())
            return self.activo

        def mostrarSensoresDeLinea():
            izq, der = unRobot.getLine()
            self.ui.iline.display(  '%0.2f' %   izq)
            self.ui.dline.display( '%0.2f' %   der)
            return self.activo

        pilas.escena_actual().tareas.condicional(3, mostrarBateria)
        pilas.escena_actual().tareas.condicional(1, mostrarPing)
        pilas.escena_actual().tareas.condicional(1, mostrarSensoresDeLinea)

       
