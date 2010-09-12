# -*- encoding: utf-8 -*-
import pilas


actor = pilas.actores.Tortuga()
animacion = pilas.imagenes.Grilla("pingu.png", 10)
animacion.asignar(actor)

texto = pilas.actores.Texto("Pulse el botón del mouse para avanzar de cuadro.")
texto.magnitud = 20
texto.x = 30
texto.y = -220

def avanzar_cuadro(*k, **kv):
    "Avanza un cuadro de animación."
    animacion.avanzar()
    animacion.asignar(actor)

pilas.eventos.click_de_mouse.connect(avanzar_cuadro)
pilas.ejecutar()
