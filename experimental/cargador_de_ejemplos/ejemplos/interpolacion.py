import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
mono = pilas.actores.Mono()
mono.x = 0
mono.y = 0
mono.rotacion = pilas.interpolar(360, duracion=3)
mono.escala = pilas.interpolar(2, duracion=3)
mono.x = pilas.interpolar(320, duracion=3)
mono.y = pilas.interpolar(240, duracion=3)

pilas.avisar("Un ejemplo de interpolacion en dos dimensiones.")
pilas.ejecutar()

