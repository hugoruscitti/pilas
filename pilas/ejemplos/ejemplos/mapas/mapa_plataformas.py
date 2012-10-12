import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

class DistanciaAlSuelo(pilas.actores.Actor):

    def __init__(self, mapa):
        pilas.actores.Actor.__init__(self)
        self.pos_x = 0
        self.pos_y = 0
        self.distancia = 100
        self.pizarra = pilas.imagenes.cargar_superficie(640, 480)
        self.imagen = self.pizarra
        pilas.escena_actual().mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        self.mapa = mapa

    def cuando_mueve_el_mouse(self, evento):
        self.pos_x, self.pos_y = evento.x, evento.y
        self.distancia = self.mapa.obtener_distancia_al_suelo(evento.x, evento.y, 200)

    def actualizar(self):
        self.pizarra.limpiar()

        # self.pizarra.texto("%d" %self.distancia, 20, 30)
        x = self.pos_x + 320
        y = 240 - self.pos_y
        self.pizarra.linea(x, y, x, y + self.distancia, grosor=2)

        if self.distancia < 200:
            texto = "Distancia del suelo: %d px" %self.distancia
            self.pizarra.linea(x - 5, y + self.distancia, x + 5, y + self.distancia, grosor=2)
        else:
            texto = "No hay un suelo a menos de 200 px..."
            self.pizarra.linea(x - 5, y + self.distancia - 4, x, y + self.distancia + 4, grosor=2)
            self.pizarra.linea(x + 5, y + self.distancia - 4, x, y + self.distancia + 4, grosor=2)

        self.pizarra.texto(texto, x + 20, y + self.distancia / 2)

pilas.iniciar()

mapa = pilas.actores.Mapa(filas=15, columnas=20)
#mapa.pintar_limite_de_bloques()

mapa.pintar_bloque(10, 10, 1)
mapa.pintar_bloque(10, 11, 1)
mapa.pintar_bloque(10, 12, 1)

distancia_al_suelo = DistanciaAlSuelo(mapa)

pilas.avisar("Mueva el mouse para detectar distancias al suelo.")
pilas.ejecutar()
