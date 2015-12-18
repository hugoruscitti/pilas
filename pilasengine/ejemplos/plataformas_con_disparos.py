import pilasengine

pilas = pilasengine.iniciar()
#pilas.depurador.definir_modos(fisica=True)

pilas.reiniciar_si_cambia(__file__)

class DisparoPersonalizado(pilasengine.actores.Actor):

    def iniciar(self, x, y):
        self.imagen = "disparos/estrella.png"
        self.aprender("RebotarComoCaja")
        self.sensor = pilas.fisica.Rectangulo(self.x, self.y, 20, 20, sensor=True, dinamica=False)

    def actualizar(self):
        self.sensor.x = self.x
        self.sensor.y = self.y
        self.rotacion += 40

        if self.colisiona_con_plataforma():
            self.eliminar()
            self.sensor.eliminar()

    def colisiona_con_plataforma(self):
        for x in self.sensor.figuras_en_contacto[1:]:
            if not x.sensor:
                return True

        return False

class Protagonista(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "aceituna.png"
        self.figura = pilas.fisica.Circulo(self.x, self.y, 17,
            friccion=0, restitucion=0)

        self.figura.sin_rotacion = True
        self.figura.escala_de_gravedad = 2

        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 20, 5, sensor=True, dinamica=False)
        self.contador_puede_disparar = 0
        self.direccion = 1

    def actualizar(self):
        velocidad = 10
        salto = 15
        self.x = self.figura.x
        self.y = self.figura.y

        if self.contador_puede_disparar > 0:
            self.contador_puede_disparar -= 1

        if self.pilas.control.derecha:
            self.figura.velocidad_x = velocidad
            self.rotacion -= velocidad
            self.direccion = 1
        elif self.pilas.control.izquierda:
            self.figura.velocidad_x = -velocidad
            self.rotacion += velocidad
            self.direccion = -1
        else:
            self.figura.velocidad_x = 0

        if self.pilas.control.boton and self.contador_puede_disparar < 1:
            self.contador_puede_disparar = 10
            self.disparar()

        if self.esta_pisando_el_suelo():
            if self.pilas.control.arriba and int(self.figura.velocidad_y) <= 0:
                self.figura.impulsar(0, salto)

        self.sensor_pies.x = self.x
        self.sensor_pies.y = self.y - 20

        if self.esta_pisando_el_suelo():
            self.imagen = "aceituna.png"
        else:
            self.imagen = "aceituna_risa.png"


    def esta_pisando_el_suelo(self):
        return len(self.sensor_pies.figuras_en_contacto) > 0


    def disparar(self):
        dx = 40 * self.direccion
        disparo_nuevo = pilas.actores.DisparoPersonalizado(x=self.x + dx, y=self.y)
        disparo_nuevo.figura.empujar(40 * 2 * self.direccion, 0)



class EscenaPrincipal(pilasengine.escenas.Escena):

    def iniciar(self):
        mapa = self.pilas.actores.MapaTiled('plataformas.tmx', densidad=0,
                    restitucion=0, friccion=0, amortiguacion=0)

        p = self.pilas.actores.Protagonista()
        caja = self.pilas.actores.Caja()
        caja.aprender('arrastrable')

        self.pilas.fondos.Tarde()
        self.pilas.avisar("Pulsa la tecla Espacio para disparar")


pilas.actores.vincular(Protagonista)
pilas.actores.vincular(DisparoPersonalizado)

pilas.escenas.vincular(EscenaPrincipal)
pilas.escenas.EscenaPrincipal()

pilas.ejecutar()
