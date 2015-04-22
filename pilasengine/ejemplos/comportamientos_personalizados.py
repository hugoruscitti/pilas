# coding: utf-8
import sys

sys.path.append('./')
sys.path.append('../')
sys.path.append('../..')

import pilasengine

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)    # reinicia pilas automaticamente cuando se edita el archivo.


class DarUnGiroCompleto(pilasengine.comportamientos.Comportamiento):
    
    def iniciar(self, receptor):
        self.receptor = receptor
        self.contador = 0
    
    def actualizar(self):
        self.contador += 5
        
        self.receptor.rotacion = self.contador
        
        if self.contador >= 360:
            return True
        
class Desaparecer(pilasengine.comportamientos.Comportamiento):
    
    def iniciar(self, receptor):
        self.receptor = receptor
    
    def actualizar(self):
        if self.receptor.transparencia < 100:
            self.receptor.transparencia += 1


# Vinculamos las habilidades personalizadas para poder utilizarlas.
pilas.comportamientos.vincular(DarUnGiroCompleto)
pilas.comportamientos.vincular(Desaparecer)


aceituna = pilas.actores.Aceituna()

aceituna.hacer("DarUnGiroCompleto")
aceituna.hacer("Avanzar", 200)
aceituna.hacer("DarUnGiroCompleto")
aceituna.hacer("Avanzar", 50)
aceituna.hacer("Desaparecer")


mono = pilas.actores.Mono(y=100)
mono.hacer("DarUnGiroCompleto")
mono.hacer("Desaparecer")



pilas.ejecutar()
