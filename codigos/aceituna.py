import pilas

class Aceituna(pilas.actores.Aceituna):

    def __init__(self):
        pilas.actores.Aceituna.__init__(self)
        self.aprender(pilas.habilidades.SeguirAlMouse)
        pilas.mundo.motor.ocultar_puntero_del_mouse()
