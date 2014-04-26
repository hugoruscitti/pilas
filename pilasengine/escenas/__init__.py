# -*- encoding: utf-8 -*-

class Escenas(object):
    """Representa la propiedad pilas.escenas

    Este objeto se encarga de hacer accesibles
    todas las escenas que incluye pilas.

    Por ejemplo, cuando un programador escribe
    "pilas.escenas.Normal()", en realidad está
    llamando a un método llamado Normal() que
    retorna un objeto escena listo para
    utilizar.
    """

    def __init__(self, pilas):
        self.pilas = pilas
        self.pila_de_escenas = []
        self.escena_actual = None

    def definir_escena(self, escena):
        self.pilas.log("Definiendo como activa la escena", escena)
        self.escena_actual = escena
        escena.iniciar()
        return escena

    def obtener_escena_actual(self):
        return self.escena_actual

    def realizar_actualizacion_logica(self):
        escena = self.obtener_escena_actual()
        escena.actualizar_actores()
        escena.actualizar_interpolaciones()
        escena.actualizar()

    def realizar_dibujado(self, painter):
        escena = self.obtener_escena_actual()
        escena.dibujar_actores(painter)

    def Normal(self):
        import normal
        nueva_escena = normal.Normal(self.pilas)
        return self.definir_escena(nueva_escena)

    def Error(self, mensaje_error):
        import error
        nueva_escena = error.Error(self.pilas, mensaje_error)
        return self.definir_escena(nueva_escena)