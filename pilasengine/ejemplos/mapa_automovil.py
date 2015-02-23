# coding: utf-8
import pilasengine

pilas = pilasengine.iniciar()


class Auto(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "auto.png"
        self.aprender('moversecomocoche')
        self.figura_de_colision = self.pilas.fisica.Rectangulo(0, 0, 40, 70)
        self.z = -10

    def actualizar(self):
        pass

    def obtener_velocidad(self):
        habilidad = self.obtener_habilidad('moversecomocoche')
        return habilidad.velocidad



pilas.actores.vincular(Auto)

protagonista = pilas.actores.Auto()


# Mueve la camara aplicando zoom a la pantalla cuando
# el auto aumenta de velocidad
def mover_camara(evento):
    pilas.camara.x = protagonista.x
    pilas.camara.y = protagonista.y
    velocidad = protagonista.obtener_velocidad()
    # Cambia el zoom de la camara, la velocidad tiene
    # valores entre 0 y 4, asi que la siguiente cuenta
    # hace que el zoom sea de 1.5 cuando el auto está detenido
    # y de 1 cuando va a su velocidad máxima.
    pilas.camara.escala = 1.5 - (velocidad/ 8.0)

pilas.eventos.actualizar.conectar(mover_camara)

#pilas.camara.escala = [0.1]


# Quita la gravedad del escenario completa y elimina
# el contenedor del escenario (piso, paredes y techo)
pilas.fisica.definir_gravedad(0, 0)

pilas.fisica.eliminar_paredes()
pilas.fisica.eliminar_techo()
pilas.fisica.eliminar_suelo()

caja1 = pilas.actores.Caja(x=+100, y=-200)
caja2 = pilas.actores.Caja(x=-200, y=100)
caja3 = pilas.actores.Caja(x=+100, y=200)

pilas.avisar("Puedes mover el auto con las flechas del teclado.")

fondo = pilas.actores.MapaTiled('calle.tmx')
fondo.z = 100

pilas.fondos.Cesped()


# Mantiene en ejecución el juego.
pilas.ejecutar()
