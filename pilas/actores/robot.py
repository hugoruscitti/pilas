# -*- encoding: utf-8 -*-

import pilas
import time
import sys

from pilas.actores import Actor
from pilas.fondos import  *
from pilas.actores import Pizarra
# from pilas.utils import distancia_entre_radios_de_colision_de_dos_actores
from PyQt4 import QtGui, QtCore, uic



# -*- encoding: utf-8 -*-


import time
import Image

from PyQt4 import QtGui
from pilas.fondos import *
from pilas.actores import Pizarra
from pilas.actores import Ejes
from datetime import datetime, timedelta

EPSILON = 0.0001

def _puntos_de_la_linea(unActor):
		
    x2, y2 = _puntosParaLaRecta(unActor)
    if (unActor.x == x2):
        linea["a"] = 1
        linea["b"] = 0
   #     linea["c"] = 1  unActor.x * (-1)
    else:
        linea["b"] = 1
        linea["a" ] = (unActor.x - x2) / (unActor.y - y2)
        linea["c" ] =  (a * unActor.x) / (b * unActor.y)
  
    return linea

def _puntoEInterseccionConLaLinea(puntoX, puntoY, pendienteM ):
# ok

    linea["a"] = pendienteM * -1
    linea["b"] = 1
    linea["c"]  = ( (lineaA * puntoX)  + (lineaB * puntoY) ) * -1
    return linea
	
def _sonParalelas(linea1, linea2):

	return ((fabs(linea1["a"] - linea2["a"]) <= EPSILON )and (fabs(linea1["b"] -linea2["b"]) <= EPSILON ))

def _sonCoincidentes(linea1, linea2):

	return(( _sonParalelas(linea1, linea2))  and (fabs(linea1["c"] - linea2["c"]) <= EPSILON ))
	
def _interseccionEntreLineas(linea1, linea2):
	
	# if  (_sonCoincudentes(linea1, linea2)):
	#	return (0,0)
	
    if (_sonParalelas(linea1, linea2)):
        return None
	
    px = ((linea2["b"] * linea1["c"] ) - (linea1["b"] * linea2["c"])) / ( (linea2["a"] * linea1["b"] ) - (linea2["b"] * linea1["a"] )   )
	
    if fabs(linea1["b"] > EPSILON): #lineas erticales
        py =  -1 * ( linea1["a"] * (px + linea1["c"]) / linea1["b"])
    else:
        py = -1 * (linea2["a"]  * (px + linea2["c"] ) / linea2["c"])
			
    return (px, py)		
	
def puntoCercaDeLaRecta(px, py, linea):		
	
	if ( fabs(linea["b"]) < EPSILON):
		# linea vertical
		px_c = -1 * linea["c"]
		py_c = py
	
	if ( fabs(linea["a"]) < EPSILON):	
		# linea horizontal
		px_c = px
		py_c = -1 * linea["c"]
	
	pendiente = 1 / linea["a"]
	
	perpendicular = _puntoEInterseccionConLaLinea(px, py, pendiente)
	
	return _interseccionEntreLineas(linea, perpendicular)
	
		
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


#### Robot

class Robot():

    def __init__(self,board, robotid=0, x=0, y=0):

       
        self.actor = pilas.actores.Tortuga()
        
        # Se le cambia la imagen
        imagen = pilas.imagenes.cargar('RobotN6.png')
        self.actor.set_imagen(imagen)
        

        self.actor.rotacion = 270
        self.actor.velocidad = 3
        self.actor.pasos = 1
        self.actor.anterior_x = x
        self.actor.anterior_y = y
        self.actor.bajalapiz()
        self.actor.aprender(pilas.habilidades.Arrastrable)
        self.actor.radio_de_colision = 31
        self.actor.color = pilas.colores.negro
        self.actor.bajalapiz()
        self.actor.tiempo = 0
#       self.actor.aprender(pilas.habilidades.SeguidoPorLaCamara)
        self.actor.aprender(pilas.habilidades.SeMantieneEnPantalla)

        """ Inicializa el robot y lo asocia con la placa board. """

        self.robotid = robotid
        self.board = board
        self.name = ''
        self.board.agregarRobot(self)
        self.tarea = None

    # Redefinir el método eliminar de la clase Actor para que lo elimine también de la lista de robots de Board
    def eliminar(self):
        self.board.eliminarDeLaLista(self)
        Actor.eliminar(self.actor)

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


    def beep(self, freq=200, seconds=0):
        """ Hace que el robot emita un pitido con frecuencia freq durante seconds segundos."""

        amplitud = 58
        sample = 8000
        half_period = int(sample/freq / 2)
        beep = chr(amplitud)*half_period+chr(0)*half_period
        beep *= int(seconds * freq)
        audio = file('/dev/audio', 'wb')
        audio.write(beep)
        audio.close()

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

## Sensores
## Cuadrantes:      xy
          #   1  -> ++
          #   2  -> +-
          #   3  -> --
          #   4  -> -+
    def _actores_cuadrante_1(self):
        actores = []
        # print "dentro de cuadrante 1"
        for actor in pilas.escena_actual().actores:
            # print actor
            if ((id(actor) != id(self.actor)) and  ((actor.x >= self.actor.x) and (actor.y >= self.actor.y)) and _actor_no_valido(actor)):
                actores.append(actor)
                # print actor
        return actores

    def _actores_cuadrante_2(self):
        actores = []
        # print "dentro del cuadrante 2"
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self.actor)  and  (actor.x >= self.actor.x and actor.y <= self.actor.y) and _actor_no_valido(actor)):
                    actores.append(actor)
        return actores

    def _actores_cuadrante_3(self):
        # print "dentro del cuadrante 3"
        actores = []
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self.actor) and (actor.x <= self.actor.x and actor.y <= self.actor.y) and _actor_no_valido(actor)):
                    actores.append(actor)
        return actores

    def _actores_cuadrante_4(self):
        # print "dentro del cuadrante 4"
        actores = []
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self.actor) and (actor.x <= self.x and actor.y >= self.actor.y) and _actor_no_valido(actor)):
                    actores.append(actor)
        return actores

    def _buscarActoresEnCadaCuadrante(self, cuadrante):
        actores = []

        if cuadrante == 1 :
            # print " _buscarActoresEnCadaCuadrante 1"
            actores = self._actores_cuadrante_1()
        elif cuadrante == 2:
            actores = self._actores_cuadrante_2()
            # print " _buscarActoresEnCadaCuadrante 2"
        elif cuadrante == 3:
            actores = self._actores_cuadrante_3()
            # print " _buscarActoresEnCadaCuadrante  3 "
        else:
            actores = self._actores_cuadrante_4()
            # print " _buscarActoresEnCadaCuadrante   4 "
        return actores


    def _analizarDistanciaEntreActores(self):
        cua = _evaluarCuadrante(self.actor)
        # print "cuadrante del robot ", cua
        valor = 100
        actores = self._buscarActoresEnCadaCuadrante(cua)
        dis = -1

        ## Recorre la lista de actores de la escena y saca la distancia de todos los que son perpendiculares a robot
        for actor in actores:
             cuac = _evaluarCuadrante(actor)
             # print "cuadrante del actor", cuac
             actorA, actorB = _puntosParaLaRecta(actor)
             robotA, robotB = _puntosParaLaRecta(self.actor)
             # print "puntos del acto: x, y ",  actorA, actorB
             # print "puntos del actor robot x, y ",  robotA, robotB
             if (_evaluarPerpendicularidadDeObjetos(self.actor, actor, robotA, robotB, actorA, actorB)) :
                 ## Los actores tienen sus rectas perpendiculares
                  # print "Las rectas son perpendiculares"
                  actorA, actorB = _puntosParaLaRecta(actor)
                  rectaX, rectaY = self._crerLasRectasEncontrarLosPuntosEnLosQueSeCortan(actorA, actorB, actor, robotA, robotB)
                  if (self._evaluarPosicionDelPuntoDeInterseccionYElSegmentoDelActor(rectaX, rectaY, actor,  cua)):
                        # print "es un obstaculo"
                    #    dis = distancia_entre_radios_de_colision_de_dos_actores(self, actor)
                        if (dis <= valor):
                             valor = dis

        if  (dis == -1) :
           # No hay actores frente al robot
            return  -1
        else:
            return valor



    def getObstacle(self, distance=100):
        """ Devuelve True si hay un obstaculo a menos de distance
        centimetros del robot. """

        valor = self._analizarDistanciaEntreActores()
        # print valor
        if valor == -1:
            return False
        else:
            return valor <=  distance




    def _crerLasRectasEncontrarLosPuntosEnLosQueSeCortan(self, otroRobotX, otroRobotY, unActor, otroPuntoActorX, otroPuntoActorY ) :

        # if ((self.x - otroRobotX)  == 0 ):
           # El robot está en una recta vertical


### otro caso es que si el de la recta vertical es el actor,  la verificación es otra


           # entonces no necesito sacar la intersección
        # Recta robot
        pendienteRobot = (self.actor.y - otroRobotY ) / (self.actor.x - otroRobotX )
        independienteRobat = ( pendienteRobot * pendienteRobot ) - self.actor.y
        # ecuación: y = pendienteRobot.x + independienteRobat

        # Recta Actor
        pendienteActor = (unActor.y - otroPuntoActorY ) / ( unActor.x - otroPuntoActorX )
        independienteActor = pendienteActor  *  pendienteActor  - unActor.y

        # Determinar el valor en que se cortan las rectas
        # Sacar el valor de X
        x = independienteRobat - independienteActor
        indep = independienteRobat - independienteActor
        valorX = x / indep

        # Sacar el valor de Y
        valorY = (pendienteRobot * valorX)  +  independienteRobat

        # Devolver los puntos en los que se corta las rectas

        return (valorX, valorY)


    def _evaluarPosicionDelPuntoDeInterseccionYElSegmentoDelActor(self, puntoX, puntoY, unActor, cuadrante):
        # Ya se que son perpendiculares y también conozco el punto en que se interconectan
        print cuadrante
        print "punto donde se sruzan los puntos", puntoX, puntoY

        if ( (cuadrante == 1 ) ):
            return ((puntoX >= unActor.x - unActor.radio_de_colision ) and ( puntoX <= unActor.x + unActor.radio_de_colision))
        else:
            return ((puntoY >= unActor.y - unActor.radio_de_colision) and (puntoY <= unActor.y + unActor.radio_de_colision))


    def actoresEnLaEscena(self):
        # print "dentro del cuadrante 4"
        actores = []
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self.actor) and _actor_no_valido(actor)):
                actores.append(actor)
        return actores


    def ping(self):
        """ Devuelve la distancia en centimetros al objeto frente al robot. """
        linea1 = _puntos_de_la_linea(self)
        
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self.actor) and _actor_no_valido(actor)):
                linea2 = _puntoEInterseccionConLaLinea(actor.x, actor.y, linea1["a"])
                ix, iy = _interseccionEntreLineas(linea1, linea2)
                if (ix!= None and iy != None):
		#			distancia = distancia_entre_radios_de_colision_de_dos_actores(self.actor, actot)
					print actor, distancia
 
   #     return self._analizarDistanciaEntreActores()
        

    def _determinar_pixel_por_cuadrante(self, cuadrante):
        if cuadrante == 1 :

            return (self.actor.x - 2, self.actor.y + 30, self.actor.x + 2, self.actor.y + 30)
        else:
            if cuadrante == 2:
                return (self.actor.x + 30, self.actor.y + 2, self.actor.x + 30, self.actor.y - 2)
            else:
                if cuadrante == 3:
                    return (self.actor.x + 2, self.actor.y - 30, self.actor.x - 2, self.actor.y - 30)
                else:
                    return (self.actor.x - 30, self.actor.y - 2, self.actor.x - 30, self.actor.y + 2)


    def getLine(self):
        """ Devuelve los valores de los sensores de linea. """

        ancho, alto =  pilas.mundo.get_gestor().escena_actual().get_fondo().dimension_fondo()
        xa, ya, xb, yb =self._determinar_pixel_por_cuadrante(_evaluarCuadrante(self.actor))

        vi = 0
        ximagen = ancho / 2 + xa
        yimagen = alto / 2 - ya
        valores = pilas.mundo.get_gestor().escena_actual().get_fondo().informacion_de_un_pixel(ximagen, yimagen)
        for i in valores:
             vi = vi + i

        vd = 0
        ximagen = ancho / 2 + xb
        yimagen = alto / 2 - yb
        valores = pilas.mundo.get_gestor().escena_actual().get_fondo().informacion_de_un_pixel(ximagen, yimagen)
        for i in valores:
            vd = vd + i

        return (vi / 3.0 , vd / 3.0)

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




