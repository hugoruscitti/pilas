# -*- encoding: utf-8 -*-
import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()

actor = pilas.actores.Actor()
animacion = pilas.imagenes.cargar_grilla("pingu.png", 10)
animacion.asignar(actor)

def avanzar_cuadro(*k, **kv):
    "Avanza un cuadro de animación."
    animacion.avanzar()
    animacion.asignar(actor)

pilas.eventos.click_de_mouse.connect(avanzar_cuadro)
pilas.avisar("Pulse el boton del mouse para avanzar un cuadro.")
pilas.ejecutar()
