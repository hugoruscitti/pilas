# coding: utf-8
import sys


sys.path.append('./')


import pilasengine

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)    # reinicia pilas automaticamente cuando
                                       # se edita y guarda este archivo.

class EscenaIntro(pilasengine.escenas.Escena):

    def iniciar(self, titulo):
        self.logotipo = pilas.actores.Texto("Introduccion a: " + titulo)
        self.texto_contador = pilas.actores.Texto("", y=-100)
        self.pilas.fondos.Pasto()
        self.contador = 0

        self.logotipo.escala = 0
        self.logotipo.rotacion = 180
        self.logotipo.escala = [1], 2
        self.logotipo.rotacion = [0], 2

    def actualizar(self):
        self.contador += 1
        self.texto_contador.texto = str(self.contador)

        if self.contador > 60 * 5: # si pasaron 5 segundos, cambia de escena.
            self.logotipo.eliminar()
            escena = pilas.escenas.EscenaMenu()

class EscenaMenu(pilasengine.escenas.Escena):

    def iniciar(self):
        self.pilas.fondos.Cesped()
        self.menu = pilas.actores.Menu(opciones=[
            ('Ir al juego', self.juego),
            ('Volver a la intro' , self.volver),
        ])

    def volver(self):
        self.pilas.escenas.EscenaIntro("mi juego")

    def juego(self):
        self.pilas.escenas.EscenaJuego()

class EscenaJuego(pilasengine.escenas.Escena):

    def iniciar(self):
        self.pilas.avisar("Pulsa ESC para regresar al menu")
        self.pilas.eventos.pulsa_tecla_escape.conectar(self.regresar_al_menu)
        self.pilas.fondos.Galaxia()
        self.pilas.actores.NaveRoja()

    def regresar_al_menu(self, evento):
        self.pilas.escenas.EscenaMenu()


pilas.escenas.vincular(EscenaIntro)
pilas.escenas.vincular(EscenaMenu)
pilas.escenas.vincular(EscenaJuego)

escena = pilas.escenas.EscenaIntro("mi juego")


pilas.ejecutar()
