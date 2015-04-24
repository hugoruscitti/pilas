# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.actores.actor import Actor
from pilasengine.actores.bala import Bala


class Torreta(Actor):
    "Representa una torreta que puede disparar y rota con el mouse." 
    
    def iniciar(self, municion_bala_simple=None, enemigos=[], cuando_elimina_enemigo=None, x=0, y=0, frecuencia_de_disparo=10):
        """Inicializa la Torreta.                                                
                                                                                 
        :param municion_bala_simple: Indica el tipo de munición que se utilizará.
        :param enemigos: Lista o grupo de enemigos que podría eliminar la torreta.
        :param x: Posición horizontal inicial.                                   
        :param y: Posición vertical inicial.                                     
        :param frecuencia_de_disparo: Frecuencia con la que se dispararán las municiones.
        """
        self.imagen = self.pilas.imagenes.cargar('torreta.png')
        self.radio_de_colision = 15

        if municion_bala_simple is None:
            municion_bala_simple = Bala

        self.aprender(self.pilas.habilidades.RotarConMouse, lado_seguimiento="arriba")
        
        self.aprender("DispararConClick",
                      municion=municion_bala_simple,
                      grupo_enemigos=enemigos,
                      cuando_elimina_enemigo=cuando_elimina_enemigo,
                      frecuencia_de_disparo=frecuencia_de_disparo,
                      angulo_salida_disparo=90,
                      distancia=27)
        
    def get_municion(self):                                                      
        """Retorna la munción que está utilizando la torreta."""                 
        return self.habilidades.DispararConClick.municion                        
                                                                                 
    def set_municion(self, municion):                                            
        """Define la munición que utilizará la torreta."""                       
        self.habilidades.DispararConClick.municion = municion                    
                                                                                 
    municion = property(get_municion, set_municion, doc="Define la munición de la torreta.")
