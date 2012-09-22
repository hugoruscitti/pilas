# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
import pilas
from pilas import tareas, colisiones, pytweener, camara
from pilas.eventos import Evento


class EscenaBase(object):
    def __init__(self):
        
        # Para controlar las escenas en el debug
        self.id = ""

        # Actores de la escena
        self.actores = []
        
        # Camara de la escena
        self.camara = camara.Camara(self)
        
        # Eventos asociados a la escena
        self.mueve_camara = Evento('mueve_camara')               # ['x', 'y', 'dx', 'dy']
        self.mueve_mouse = Evento('mueve_mouse')                 # ['x', 'y', 'dx', 'dy']
        self.click_de_mouse = Evento('click_de_mouse')           # ['button', 'x', 'y']
        self.termina_click = Evento('termina_click')             # ['button', 'x', 'y']
        self.mueve_rueda = Evento('mueve_rueda')                 # ['delta']
        self.pulsa_tecla = Evento('pulsa_tecla')                 # ['codigo', 'texto']
        self.suelta_tecla = Evento('suelta_tecla')               # ['codigo', 'texto']
        self.pulsa_tecla_escape = Evento('pulsa_tecla_escape')   # []
        
        # Gestor de tareas
        self.tareas = tareas.Tareas()
        
        # Gestor de colisiones
        self.colisiones = colisiones.Colisiones()
        
        self.tweener = pytweener.Tweener()
        
        self.fisica = pilas.mundo.crear_motor_fisica()
        
    def iniciar(self):
        raise Exception("Tienes que re-definir el metodo iniciar.")
        
    def pausar(self):
        self.fisica.pausar_mundo()
    
    def reanudar(self):
        self.fisica.reanudar_mundo()
    
    def actualizar(self):
        pass
    
    """ Estos metodos no deben ser sobreescritos en las clases que
    hereden de ella.
    """
    def actualizar_eventos(self):
        self.tweener.update(16)
        self.tareas.actualizar(1/60.0)
        self.colisiones.verificar_colisiones()        
        
    def actualizar_fisica(self):
        if self.fisica:
            if len(self.fisica.mundo.bodies) > 4: # Es mayor de 4 ya que las paredes son 4 elementos.
                self.fisica.actualizar()
    
    def limpiar(self):
        for actor in self.actores:
            actor.destruir()
            
        self.tareas.eliminar_todas()
        self.tweener.eliminar_todas()
        if self.fisica:
            self.fisica.reiniciar()
    