# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
import pilas
from pilas.escena.escena_base import EscenaBase
import pilas.fondos
import pilas.colores

class EscenaNoche(EscenaBase):
    
    def __init__(self, gestor_escenas):
        EscenaBase.__init__(self, gestor_escenas)        
                
    def iniciar(self):
        fondo = pilas.fondos.Noche()
        self.mono = pilas.actores.Mono()
    
    def limpiar(self):
        pass
    
    def pausar(self):
        pass
    
    def reanudar(self):
        pass
    
    def actualizar(self):
        pass
