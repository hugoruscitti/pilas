import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()

class PizarraConectaActores(pilas.actores.Pizarra):

    def __init__(self, actor1, actor2):
        pilas.actores.Pizarra.__init__(self)
        self.actor1 = actor1
        self.actor2 = actor2

    def actualizar(self):
        x0, y0 = self.actor1.x, self.actor1.y
        x1, y1 = self.actor2.x, self.actor2.y

        self.limpiar()
        self.linea(x0, y0, x1, y1, grosor=2)

    def cuando_mueve_el_mouse(self, evento):
        if self.boton_pulsado:
            self.pizarra.linea(self.mouse_x, self.mouse_y, evento.x, evento.y, grosor=2)

        self.mouse_x = evento.x
        self.mouse_y = evento.y

a1 = pilas.actores.Aceituna(x=-200)
a2 = pilas.actores.Aceituna(x=200)
a1.aprender(pilas.habilidades.Arrastrable)
a2.aprender(pilas.habilidades.Arrastrable)

pizarra = PizarraConectaActores(a1, a2)
pizarra.z = 2

pilas.avisar("Puedes arrastrar a los personajes con el mouse.")
pilas.ejecutar()
