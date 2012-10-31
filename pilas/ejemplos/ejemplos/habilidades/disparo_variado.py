import pilas
import os

from pilas.actores.actor import Actor
from pilas.municion import BalaSimple
from pilas.municion import BalaDoble
from pilas.municion import MisilSimple
from pilas.municion import EstrellaNinjaSimple

pilas.iniciar()


def eliminar(disparo, enemigo):

    enemigo.eliminar()

    if isinstance(enemigo, pilas.actores.Banana):
        torreta.habilidades.DispararConClick.municion = BalaSimple
        torreta.habilidades.DispararConClick.frecuencia_de_disparo = 10
        torreta.habilidades.DispararConClick.escala = 1
        torreta.habilidades.DispararConClick.offset_disparo_x=27
        torreta.habilidades.DispararConClick.offset_disparo_y=27
    else:
        torreta.habilidades.DispararConClick.municion = MisilSimple
        torreta.habilidades.DispararConClick.frecuencia_de_disparo = 10
        torreta.habilidades.DispararConClick.escala = 1
        torreta.habilidades.DispararConClick.offset_disparo_x=42
        torreta.habilidades.DispararConClick.offset_disparo_y=42


municion_bala_simple = EstrellaNinjaSimple

banana = pilas.actores.Banana(x=200, y=150)
aceituna = pilas.actores.Aceituna(x=-200, y=150)

torreta = pilas.actores.Torreta(municion_bala_simple=municion_bala_simple, enemigos=[banana, aceituna],
                             cuando_elimina_enemigo=eliminar)

torreta.habilidades.DispararConClick.escala = 0.5


pilas.ejecutar()
