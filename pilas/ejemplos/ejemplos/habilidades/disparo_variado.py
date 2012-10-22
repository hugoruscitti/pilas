import pilas
import os

pilas.iniciar()

def eliminar(disparo, enemigo):
    enemigo.eliminar()
    if isinstance(enemigo, pilas.actores.Banana):
        arma.habilidades.Disparar.municion = pilas.actores.disparo.BalaSimple()
    else:
        arma.habilidades.Disparar.municion = pilas.actores.disparo.MisilSimple()
        arma.habilidades.Disparar.frecuencia_de_disparo = 1

municion = pilas.actores.disparo.DobleBalasDesviadas()

arma = pilas.actores.Actor(os.path.abspath("arma.png"))

banana = pilas.actores.Banana(x=200, y=150)
aceituna = pilas.actores.Aceituna(x=-200, y=150)

arma.aprender(pilas.habilidades.RotarConMouse,
              lado_seguimiento=pilas.habilidades.RotarConMouse.ARRIBA)

arma.aprender(pilas.habilidades.DispararConClick,
              municion=municion,
              grupo_enemigos=[banana,aceituna],
              cuando_elimina_enemigo=eliminar,
              frecuencia_de_disparo=10,
              angulo_salida_disparo=0,
              offset_disparo=(27,27))

pilas.ejecutar()
