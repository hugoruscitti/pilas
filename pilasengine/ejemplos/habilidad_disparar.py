# -*- encoding: utf-8 -*-
import pilasengine

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)

class MiMunicion(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "disparos/bola_amarilla.png"
        self.escala_y = 0.25
        self.escala_x = 0.25
        self.y = 100
    
    def actualizar(self):
        # actualizar se ejecuta 60 veces por segundo, así
        # que las siguientes lineas harán que aumente el tamaño
        # del diparo y siempre estén girando.
        self.escala_y += 0.2
        self.rotacion += 10

pilas.actores.vincular(MiMunicion)

# Construye al protagonista y le permite utilizar
# al nuevo actor como munición de disparo.
aceituna = pilas.actores.Aceituna()
aceituna.aprender('disparar', municion='MiMunicion', angulo_salida_disparo=90)
aceituna.aprender('moversecomocoche')

pilas.avisar("Pulsa la tecla espacio para disparar.")
pilas.ejecutar()
