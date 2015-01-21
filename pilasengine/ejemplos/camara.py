import pilasengine
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas = pilasengine.iniciar()

mono = pilas.actores.Mono()
mono.escala = 1
mono.rotacion = 0

def girar():
    mono.rotacion = mono.rotacion + 1
    return True

pilas.escena.tareas.siempre(0.01, girar)

pilas.escena_actual().camara.x = [200, 0], 10
pilas.escena_actual().camara.y = [200, 0], 10

pilas.avisar("Moviendo la camara...")
pilas.ejecutar()
