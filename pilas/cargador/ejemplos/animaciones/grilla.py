# -*- encoding: utf-8 -*-
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas


pilas.iniciar()

actor = pilas.actores.Actor()
imagen = pilas.imagenes.cargar_grilla("pingu.png", 10)
actor.imagen = imagen

def avanzar_cuadro(*k, **kv):
    "Avanza un cuadro de animación."
    imagen.avanzar()
    actor.imagen = imagen

pilas.eventos.click_de_mouse.connect(avanzar_cuadro)
pilas.avisar("Pulse el boton del mouse para avanzar un cuadro.")
pilas.ejecutar()
