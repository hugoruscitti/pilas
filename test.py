import pilasengine

pilas = pilasengine.iniciar()

class MiActor(pilasengine.actores.Actor):

    def iniciar(self, nombre, apellido, test=123):
        print "soy un actor de nombre", nombre, "y apellido", apellido

MiActor(pilas, 0, 0, None, "pepe")
pilas.ejecutar()
