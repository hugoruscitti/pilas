# -*- encoding: utf-8 -*-
import pilasengine

pilas = pilasengine.iniciar()

class EscenaMenu(pilasengine.escenas.Escena):

    def iniciar(self):
        self.pilas.fondos.FondoMozaico('imagenes/azul.png')
        actor_texto = self.pilas.actores.Actor()
        actor_texto.imagen = "imagenes/click.png"
        self._aplicar_animacion(actor_texto)
        self.pilas.eventos.click_de_mouse.conectar(self._iniciar_el_juego)
        self._crear_el_titulo_del_juego()
        self._crear_indicador_creditos()

    def _aplicar_animacion(self, texto):
        texto.y = -500
        texto.escala = 4
        texto.escala = [1], 1.5
        texto.y = [-100], 1

    def _iniciar_el_juego(self, evento):
        self.pilas.escenas.EscenaJuego()

    def _crear_el_titulo_del_juego(self):
        titulo = self.pilas.actores.Actor()
        titulo.imagen = "imagenes/titulo.png"
        titulo.y = 300
        titulo.rotacion = 30
        titulo.y = [100], 1
        titulo.rotacion = [0], 1.2

    def _crear_indicador_creditos(self):
        actor = self.pilas.actores.Actor()
        actor.imagen = "imagenes/creditos.png"
        actor.x = 400
        actor.y = -200
        actor.x = [400, 400, 270], 0.5


class BotonVolver(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "imagenes/boton_volver.png"
        self.cuando_hace_click = self._volver_a_la_escena_inicial
        self.y = 300
        self.y = [200]
        self.x = -200

    def _volver_a_la_escena_inicial(self, evento):
        self.pilas.escenas.EscenaMenu()

class ActorEliminado(pilasengine.actores.Actor):
    """Representa una animación del pato muriendo."""

    def iniciar(self, x, y):
        self.imagen = "imagenes/pato_eliminado.png"
        self.x = x
        self.y = y
        self.transparencia = [100]
        self.dx = self.pilas.azar(-10, 10)
        self.dy = pilas.azar(10, 20)
        self.contador = 0

    def actualizar(self):
        self.x += self.dx
        self.y += self.dy
        self.rotacion += 30

        self.contador += 1

        if self.contador > 60:
            self.eliminar()

class ActorPato(pilasengine.actores.Actor):

    def iniciar(self):
        self.x = -400
        self.velocidad = self.pilas.azar(2, 7)
        self.imagen = "imagenes/pato.png"
        self.y = self.pilas.azar(-50, 100)
        self.z = 1

    def actualizar(self):
        self.x += self.velocidad

        # Elimina al actor si sale de la pantalla
        if self.x > 400:
            self.eliminar()

    def disparar(self):
        "Se invoca desde la escena de juego, cuando el usuario hace click sobre el pato."
        self.eliminar()
        self.pilas.camara.vibrar(1, 0.3)
        self.pilas.actores.ActorEliminado(self.x, self.y)

class EscenaJuego(pilasengine.escenas.Escena):

    def iniciar(self):
        self.pilas.fondos.FondoMozaico('imagenes/madera.png')
        self._crear_fondo()
        self._crear_boton_volver()
        self.pilas.tareas.siempre(2, self._crear_un_actor_pato)
        self.pilas.eventos.click_de_mouse.conectar(self._cuando_hace_click)
        self.puntaje = pilas.actores.Puntaje(290, 200, color="blanco")

    def _crear_boton_volver(self):
        pilas.actores.BotonVolver()

    def _crear_fondo(self):
        self.fondo_alejado = pilas.fondos.DesplazamientoHorizontal()
        self.fondo_alejado.agregar('imagenes/pasto2.png', 0, 20, 0.3)
        self.fondo_alejado.agregar('imagenes/pasto.png', 0, 80, 0.7)
        self.fondo_alejado.agregar('imagenes/agua1.png', 0, 100, 1)
        self.fondo_alejado.z = 100

        self.fondo_agua = pilas.fondos.DesplazamientoHorizontal()
        self.fondo_agua.agregar('imagenes/agua2.png', 0, 200, 2)
        self.fondo_agua.z = -100

    def actualizar(self):
        self.fondo_agua.desplazar(1)
        self.fondo_alejado.desplazar(1)

    def _crear_un_actor_pato(self):
        self.pilas.actores.ActorPato()

    def _cuando_hace_click(self, evento):
        actores_en_colision = self.obtener_actores_en(evento.x, evento.y)

        for actor in actores_en_colision:
            if isinstance(actor, ActorPato):
                actor.disparar()
                self.puntaje.aumentar()


## Vinculamos todas las escenas.
pilas.escenas.vincular(EscenaMenu)
pilas.escenas.vincular(EscenaJuego)


## Vinculamos los actores Personalizados
pilas.actores.vincular(BotonVolver)
pilas.actores.vincular(ActorPato)
pilas.actores.vincular(ActorEliminado)


# Se inicia la escena principal.
pilas.escenas.EscenaMenu()

pilas.ejecutar()
