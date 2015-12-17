import pilasengine
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas = pilasengine.iniciar()
mono = pilas.actores.Mono()
mono.x = 0
mono.y = 0
pilas.utils.interpolar(mono, 'rotacion', 360, duracion=3)
pilas.utils.interpolar(mono, 'escala', 2, duracion=3)

pilas.utils.interpolar(mono, 'x', 320, duracion=3)
pilas.utils.interpolar(mono, 'y', 240, duracion=3)

pilas.avisar("Un ejemplo de interpolacion en dos dimensiones.")
pilas.ejecutar()

