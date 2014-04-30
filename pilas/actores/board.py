# -*- encoding: utf-8 -*-
import pilas

from pilas.actores import Actor
#### Board

class Board():

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
 

