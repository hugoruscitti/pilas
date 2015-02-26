import pilasengine

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)    # reinicia pilas automaticamente cuando
                                       # se edita y guarda este archivo.

class EscenaIntro(pilasengine.escenas.Escena):

    def iniciar(self, titulo):
        print "iniciando!!"
        self.logotipo = pilas.actores.Texto("Introduccion a: " + titulo)
        self.contador = 0

    def actualizar(self):
        self.contador += 1

        if self.contador > 60 * 5: # si pasaron 5 segundos, cambia de escena.
            self.logotipo.eliminar()
            escena = pilas.escenas.EscenaMenu()

class EscenaMenu(pilasengine.escenas.Escena):

    def iniciar(self):
        self.pilas.fondos.Cesped()


pilas.escenas.vincular(EscenaIntro)
escena = pilas.escenas.EscenaIntro("inicial")


pilas.ejecutar()
