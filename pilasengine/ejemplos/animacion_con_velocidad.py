# -*- encoding: utf-8 -*-
import sys
sys.path.append('.')
import pilasengine

pilas = pilasengine.iniciar()

grilla = pilas.imagenes.cargar_grilla("explosion.png", 7)
animacion = pilas.actores.Animacion(grilla, True, velocidad=1)

texto = pilas.actores.Texto("1 cuadro por segundo", x=100, y=80, magnitud=10, ancho=200)
texto.color = pilas.colores.negro


def cambia_velocidad(progreso):
    progreso = 1 + progreso * 60.0
    animacion.velocidad_de_animacion = progreso
    texto.texto = str(int(progreso)) + " cuadros por segundo"


barra = pilas.interfaz.Deslizador(y=100)
barra.conectar(cambia_velocidad)


pilas.avisar("Usa la barra para modificar la velocidad de la animacion.")
pilas.ejecutar()
