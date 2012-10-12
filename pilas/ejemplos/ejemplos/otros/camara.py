import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()

mono = pilas.actores.Mono()
mono.escala = 1
mono.rotacion = 0

def girar():
    mono.rotacion = mono.rotacion + 1
    return True

pilas.mundo.agregar_tarea_siempre(0.01, girar)

pilas.escena_actual().camara.x = pilas.utils.interpolar([200, 0], duracion=10)
pilas.escena_actual().camara.y = pilas.utils.interpolar([200, 0], duracion=10)

pilas.avisar("Moviendo la camara...")
pilas.ejecutar()
