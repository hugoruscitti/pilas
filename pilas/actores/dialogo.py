# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas

class Dialogo:
    "Representa una secuencia de mensajes entre varios actores."
    
    def __init__(self, modo_automatico=True):
        self.dialogo = []
        self.dialogo_actual = None
        self.modo_automatico = modo_automatico
    
    def decir(self, actor, texto):
        self.dialogo.append((actor, texto))

    def decir_inmediatamente(self, actor, texto):
        self.dialogo = []
        self._eliminar_dialogo_actual()
        self.decir(actor, texto)
        siguiente = self.obtener_siguiente_dialogo_o_funcion()
        self._mostrar_o_ejecutar_siguiente(siguiente)

    def elegir(self, actor, texto, opciones, funcion_a_invocar):
        self.dialogo.append((actor, texto, opciones, funcion_a_invocar))
        
    def ejecutar(self, funcion):
        self.dialogo.append(funcion)

    def iniciar(self):
        self.avanzar_al_siguiente_dialogo()

    def obtener_siguiente_dialogo_o_funcion(self):
        if self.dialogo:
            return self.dialogo.pop(0)
        
    def _eliminar_dialogo_actual(self):
        if self.dialogo_actual:
            self.dialogo_actual.eliminar()
            self.dialogo_actual = None

    def _mostrar_o_ejecutar_siguiente(self, siguiente):
        if isinstance(siguiente, tuple):
            # Es un mensaje de dialogo simple
            if len(siguiente) == 2:
                actor, texto = siguiente
                self.dialogo_actual = pilas.actores.Globo(texto, dialogo=self, avance_con_clicks=self.modo_automatico)
            else:
                # Es un mensaje con seleccion.
                actor, texto, opciones, funcion_a_invocar = siguiente
                self.dialogo_actual = pilas.actores.GloboElegir(texto, opciones, funcion_a_invocar, dialogo=self)
                
            self.dialogo_actual.colocar_origen_del_globo(actor.x, actor.arriba)
        else:
            siguiente()
            self.avanzar_al_siguiente_dialogo()

    def avanzar_al_siguiente_dialogo(self, evento=None):
        self._eliminar_dialogo_actual()
        siguiente = self.obtener_siguiente_dialogo_o_funcion()
        
        if siguiente:
            self._mostrar_o_ejecutar_siguiente(siguiente)
        else:
            return False
            
        return True
