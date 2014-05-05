from PyQt4 import QtGui
from pilasengine.actores.actor import Actor


class Mono(Actor):

    def iniciar(self):
        self.imagen = "mono.png"
        self.sonido = self.pilas.sonidos.cargar('audio/grito.wav')

    def actualizar(self):
        pass

    def saltar(self):
        self.sonido.reproducir()