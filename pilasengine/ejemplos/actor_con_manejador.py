# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.append("..")
sys.path.append(".")
import pilasengine

pilas = pilasengine.iniciar()
actor = pilas.actores.Actor()

pilas.actores.ManejadorPropiedad(0, 200, actor, 'escala', 0.1, 3.0)

pilas.avisar("Este es un ejemplo de actor creado pero sin imagen.")
pilas.ejecutar()
