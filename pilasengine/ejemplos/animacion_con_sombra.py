# -*- encoding: utf-8 -*-
#
# Usando gráficos de Claudio Andaur, del juego "el juego de la vaca".
#
import sys
sys.path.append('.')
import pilasengine

pilas = pilasengine.iniciar()

grilla = pilas.imagenes.cargar_grilla("vaca_corriendo.png", 10)
animacion = pilas.actores.Animacion(grilla, True, velocidad=24)

actor_texto = pilas.actores.Texto(x=100, y=140)
actor_texto.texto = ""
actor_texto.ancho = 300

grilla_sombra = pilas.imagenes.cargar_grilla("sombra_vaca_corriendo.png", 10)
animacion_sombra = pilas.actores.Animacion(grilla_sombra, True, velocidad=24)
animacion_sombra.y = -65

def cambia_velocidad(progreso):
    progreso = 1 + progreso * 60.0
    animacion.velocidad_de_animacion = progreso
    animacion_sombra.velocidad_de_animacion = progreso
    actor_texto.texto = str(int(progreso)) + " cuadros por segundo"


barra = pilas.interfaz.Deslizador(x=-50, y=100)
barra.conectar(cambia_velocidad)


pilas.avisar("Usa la barra para modificar la velocidad de la animacion.")
pilas.ejecutar()