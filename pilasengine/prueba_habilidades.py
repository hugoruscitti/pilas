# coding: utf-8
import pilasengine
import math

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)    # reinicia pilas automaticamente cuando
                                       # se edita y guarda este archivo.


class AvanzaAIzquierda(pilasengine.habilidades.Habilidad):

    def iniciar(self, receptor, velocidad):
        self.receptor = receptor
        self.velocidad = velocidad

    def actualizar(self):
        self.receptor.x -= self.velocidad

        if self.receptor.x < -320:
            self.receptor.x  = 320

# En la siguiente habilidad se omitió el metodo iniciar, esto
# es lo mismo que crear un método iniciar con este contenido:
#
#      def iniciar(self, receptor):
#           self.receptor = receptor
#
# Si se le quiere dar un valor inicial a alguna variable o pasarle
# algún argumento extra se lo tiene que definir, sino no hace falta.
class RotarPorSiempre(pilasengine.habilidades.Habilidad):

    def actualizar(self):
        self.receptor.rotacion += 1

class AlternarTamano(pilasengine.habilidades.Habilidad):

    def iniciar(self, receptor, escala_inicial):
        self.contador = 0
        self.escala_inicial = escala_inicial
        self.receptor = receptor

    def actualizar(self):
        self.contador += 0.1
        self.receptor.escala = self.escala_inicial + math.cos(self.contador)/2.0


# Vinculamos todas las habilidades para poder utilizarlas.
pilas.habilidades.vincular(AvanzaAIzquierda)
pilas.habilidades.vincular(RotarPorSiempre)
pilas.habilidades.vincular(AlternarTamano)

# Creamos la primer aceituna, la que va a mostrarse en el centro
# de la pantalla.
aceituna = pilas.actores.Aceituna()

# A la primer aceituna, le enseñamos varias habilidades.
aceituna.aprender("AvanzaAIzquierda", 1)
aceituna.aprender("rotarporSiempre")
aceituna.aprender("arrastrable")
aceituna.aprender("AlternarTamano", 2)


# La segunda aceituna solo tiene la habilidad de ir a la izquierda, pero
# con una velocidad diferente.
aceituna2 = pilas.actores.Aceituna(y=200)
aceituna2.aprender("AvanzaAIzquierda", 2)

pilas.ejecutar()
