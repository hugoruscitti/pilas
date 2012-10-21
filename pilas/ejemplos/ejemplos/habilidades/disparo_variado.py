import pilas

pilas.iniciar()

def eliminar(disparo, banana):
    banana.eliminar()
    mono.habilidades.Disparar.municion = pilas.actores.disparo.BalaSimple()

municion = pilas.actores.disparo.DobleBalasDesviadas()

mono = pilas.actores.Mono()
banana = pilas.actores.Banana(x=200, y=150)

mono.aprender(pilas.habilidades.RotarConMouse)

mono.aprender(pilas.habilidades.Disparar,
              municion=municion,
              grupo_enemigos=banana,
              cuando_elimina_enemigo=eliminar,
              angulo_salida_disparo=-90)

pilas.ejecutar()