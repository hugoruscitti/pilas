# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
import pilas
from pilas.eventos import Evento


class EscenaBase(object):
    def __init__(self):
        
        # Actores de la escena
        self.actores = []
        
        # Gestor de las escenas para poder cambiar entre ellas.
        self.gestor_escenas = pilas.mundo.gestor_escenas
        
        # Eventos asociados a la escena
        self.mueve_mouse = Evento('mueve_mouse')                 # ['x', 'y', 'dx', 'dy']
        self.click_de_mouse = Evento('click_de_mouse')           # ['button', 'x', 'y']
        self.termina_click = Evento('termina_click')             # ['button', 'x', 'y']
        self.mueve_rueda = Evento('mueve_rueda')                 # ['delta']
        self.pulsa_tecla = Evento('pulsa_tecla')                 # ['codigo', 'texto']
        self.suelta_tecla = Evento('suelta_tecla')               # ['codigo', 'texto']
        self.pulsa_tecla_escape = Evento('pulsa_tecla_escape')   # []
    
        # Para controlar las escenas en el debug
        self.id = ""
    
    def iniciar(self):
        raise Exception("Tienes que re-definir el metodo iniciar método.")
    
    def limpiar(self):
        pass
    
    def pausar(self):
        pass
    
    def reanudar(self):
        pass
    
    def actualizar(self):
        pass
    