import math
import pilas


class LanzadorDeBananas:

    def __init__(self, mono_que_dispara, escena_juego):
        self.escena_juego = escena_juego
        self.mono_que_dispara = mono_que_dispara
        x = mono_que_dispara.x
        y = 200

        self.angulo = pilas.interfaz.Deslizador(x=x, y=y)
        self.fuerza = pilas.interfaz.Deslizador(x=x, y=y-30)

        self.etiqueta_1 = self._crear_etiqueta("Angulo:", self.angulo)
        self.etiqueta_2 = self._crear_etiqueta("Fuerza:", self.fuerza)

        self.boton = pilas.interfaz.Boton("Disparar !", x=x, y=y-80)
        self.boton.conectar(self.cuando_pulsa_disparar)

    def _crear_etiqueta(self, texto, deslizador):
        actor_texto = pilas.actores.Texto(texto, magnitud=10, y=deslizador.y)
        actor_texto.derecha = deslizador.izquierda - 20
        return actor_texto

    def eliminar(self):
        self.angulo.eliminar()
        self.fuerza.eliminar()
        self.etiqueta_1.eliminar()
        self.etiqueta_2.eliminar()
        self.boton.desactivar()
        self.boton.eliminar()

    def cuando_pulsa_disparar(self):
        angulo = 180 - self.angulo.progreso * 180
        fuerza = (1 + self.fuerza.progreso) * 2

        self.escena_juego.disparar(self.mono_que_dispara.x, self.mono_que_dispara.y, angulo, fuerza)


class Banana(pilas.actores.Banana):

    def __init__(self, *k, **kv):
        pilas.actores.Banana.__init__(self, *k, **kv)
        self.escala = 0.5
        self.dx = 0
        self.dy = 0
        self._vel_y = 3

    def actualizar(self):
        self.rotacion += 10
        self.x += self.dx
        self.y += self.dy + self._vel_y
        self._vel_y -= 0.1

    def lanzar(self, angulo, fuerza):
        angulo_en_radianes = math.radians(angulo)
        self.dx = math.cos(angulo_en_radianes) * fuerza
        self.dy = math.sin(angulo_en_radianes) * fuerza


class EscenaJuego(pilas.escena.Normal):

    def iniciar(self):
        self._crear_monos()
        self.turno = 2
        self.lanzador = None
        self.cambiar_turno()

    def _crear_monos(self):
        self.mono1 = self._crear_mono(x=-200)
        self.mono2 = self._crear_mono(x=200)

    def _crear_mono(self, x=0, y=0):
        mono = pilas.actores.Mono(x, y)
        mono.escala = 0.4
        return mono

    def cambiar_turno(self):
        mono = None

        if self.turno == 2:
            self.turno = 1
            mono = self.mono1
        else:
            self.turno = 2
            mono = self.mono2

        mono.decir("Es mi turno!")

        if self.lanzador:
            self.lanzador.eliminar()

        self.lanzador = LanzadorDeBananas(mono, self)

    def disparar(self, desde_x, desde_y, angulo, fuerza):
        banana = Banana(desde_x, desde_y)
        banana.lanzar(angulo, fuerza)
        self.cambiar_turno()

pilas.iniciar()
escena_de_juego = EscenaJuego()
pilas.cambiar_escena(escena_de_juego)
pilas.ejecutar()
