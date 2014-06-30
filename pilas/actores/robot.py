# -*- encoding: utf-8 -*-

import pilas
import time
import sys
import utils
import math



from pilas.actores import Actor
from pilas.fondos import  *
from pilas.actores import Pizarra
from pilas.actores import Nave
# from pilas.utils import distancia_entre_radios_de_colision_de_dos_actores
from PyQt4 import QtGui, QtCore, uic
import weakref

import Image

from PyQt4 import QtGui
from pilas.fondos import *
from pilas.actores import Ejes
from datetime import datetime, timedelta

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
        print "No es vertical u horizontal"
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

def puntoCercaDeLaRecta(px, py, linea):		

    if ( fabs(linea["B"]) < EPSILON):
    # linea vertical
        px_c = -1 * linea["C"]
        py_c = py
        
    if ( fabs(linea["A"]) < EPSILON):	
	# linea horizontal
        px_c = px
        py_c = -1 * linea["C"]

    pendiente = 1 / linea["A"]
    perpendicular = _puntoEInterseccionConLaLinea(px, py, pendiente)
    return _interseccionEntreLineas(linea, perpendicular)




def _actor_no_valido(actor):
    return (not isinstance(actor, Pizarra) and (not isinstance(actor, Fondo)) and  (not isinstance(actor, Ejes)))

def wait(seconds = 0):
    """ Produce un retardo de seconds segundos en los que el robot no hace nada. """

    now = datetime.now()
    while now + timedelta(0, seconds, 0) > datetime.now():
        QtGui.QApplication.processEvents()



#### Robot

class Robot():

    def __init__(self,board, robotid=0, x=0, y=0):
        """ Inicializa el robot y lo asocia con la placa board. """

        self.actor = NaveTortuga()

        # Se queda en pantalla
        self.actor.aprender(pilas.habilidades.SeMantieneEnPantalla)

        self.radio_de_colision = self.actor.radio_de_colision
        self.robotid = robotid
        self.board = board
        self.name = ''
        self.proxy = weakref.proxy(self)
        self.board.agregarRobot(self.proxy)
        self.tarea = None
        self.obstaculos = None
        self.observar = False


    # Redefinir el método eliminar de la clase Actor para que lo elimine también de la lista de robots de Board
    def eliminar(self):
        self.board.eliminarDeLaLista(self.proxy)
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


    def getObstacle(self, distance=100):
        """ Devuelve True si hay un obstaculo a menos de distance
        centimetros del robot. """
        valor =  self.ping()
        print "valor",valor
        if (valor <= distance):
			
            return True
        else:
            return False

    def ping(self):
        """ Devuelve la distancia en centimetros al objeto frente al robot. """
        self.ultimo_ping = -1
        
        actores = self.actor.actoresEnLaEscena()

        self.actor.definir_enemigos(actores)
        
        return self.actor.disparar()
        
        #if (self.ultimo_ping != -1):
            #return self.ultimo_ping
        #else:
	    
        
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
        self.acto.x = valor
    
    def get_x(self):
        return self.acto.x
        
    def set_y(self, valor):
        self.actor.x = valor
        
    def get_y(self):
        return self.acto.y
        
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    
    
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


class NaveTortuga(Nave):
    # Por Nave

    def __init__(self, x=0, y=0, velocidad=2):

        imagen = pilas.imagenes.cargar('RobotN6.png')
        Actor.__init__(self, imagen, x=x, y=y)

        self.municion = pilas.actores.Bala
        self.esta_disparando = False
        self.bajalapiz()
        self.ultimo_ping = -1
        self.rotacion = 270
        self.velocidad = 3
        self.pasos = 1
        self.anterior_x = x
        self.anterior_y = y
        self.bajalapiz()
        self.pizarra = pilas.actores.Pizarra()

        self.aprender(pilas.habilidades.Arrastrable)
        self.radio_de_colision = 31
        self.color = pilas.colores.negro

        self.aprender(pilas.habilidades.Disparar,
                       municion= self.municion,
                       parametros_municion = { "self.x": self.x, "y": self.y, "angulo_de_movimiento" : self.rotacion, "rotacion": self.rotacion },
                       angulo_salida_disparo= self.rotacion, 
                       frecuencia_de_disparo=3,
                       offset_disparo=(self.x,self.y),
                       escala=0.7)

    def obtenerDistancia(self, mi_disparo, el_enemigo):
        self.ultimo_disparo = mi_disparo
        self.ultimo_ping = pilas.utils.distancia_entre_radios_de_colision_de_dos_actores (el_enemigo, self)
        print  "en elobtenerDistancia ",  self.ultimo_ping
        mi_disparo.eliminar()
        return self.ultimo_ping
        
       
    def actoresEnLaEscena(self):

        actores = []
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self) and _actor_no_valido(actor)):
                actores.append(actor)
        return actores
    
		
    def disparando(self):
        def ir_disparando():
            self.disparar()
            return (self.esta_disparando)

        self.esta_disparando = True
        self.tarea = pilas.escena_actual().tareas.condicional(0.1, ir_disparando) 

    def disparar(self):
        for x in self._habilidades:
            if x.__class__.__name__ == 'Disparar':
                self.ultimo_ping  = x.disparar()
        
        

    def definir_enemigos(self, grupo, cuando_elimina_enemigo=None):
        """Hace que una nave tenga como enemigos a todos los actores del grupo.

        :param grupo: El grupo de actores que serán sus enemigos.
        :type grupo: array
        :param cuando_elimina_enemigo: Funcion que se ejecutará cuando se elimine un enemigo.

        """
        self.cuando_elimina_enemigo = cuando_elimina_enemigo
        self.habilidades.Disparar.definir_colision(grupo, self.obtenerDistancia)    

   ## Por Tortuga

    def bajalapiz(self):
        """Le indica a la tortuga si debe comenzar a dibujar con cada movimiento."""
        self.lapiz_bajo = True

    def subelapiz(self):
        """Le indica a la tortuga que deje de dibujar con cada movimiento."""
        self.lapiz_bajo = False
        
    def get_color(self):
        """Retorna el color que se utilizará para trazar."""
        return self._color

    def set_color(self, color):
        """Define el color que se utilizará para trazar.

        :param color: El color a utilizar.
        """
        self._color = color

    color = property(get_color, set_color)

    def pintar(self, color=None):
        """Pinta todo el fondo de un solo color.

        :param color: El color que se utilizará para pintar el fondo.
        """
        self.pizarra.pintar(color)

    def actualizar(self):
        """Actualiza su estado interno."""
        if self.anterior_x != self.x or self.anterior_y != self.y:
            if self.lapiz_bajo:
                self.dibujar_linea_desde_el_punto_anterior()
            self.anterior_x = self.x
            self.anterior_y = self.y

    def dibujar_linea_desde_el_punto_anterior(self):
        """Realiza el trazado de una linea desde su posición actual hacia la anterior."""
        self.pizarra.linea(self.anterior_x, self.anterior_y, self.x, self.y, self.color, grosor=4)

    def pon_color(self, color):
        """Define el color de trazado cuando comienza a moverse."""
        self.color = color
