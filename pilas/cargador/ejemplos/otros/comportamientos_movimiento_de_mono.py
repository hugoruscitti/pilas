import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()
mono = pilas.actores.Mono()

pasos = 3

mono.x = -50
mono.y = -50

mono.hacer_luego(pilas.comportamientos.Avanzar(90, pasos))
mono.hacer_luego(pilas.comportamientos.Girar(180, 10))
mono.hacer_luego(pilas.comportamientos.Avanzar(180, pasos))
mono.hacer_luego(pilas.comportamientos.Girar(-180, 10))
mono.hacer_luego(pilas.comportamientos.Avanzar(180, pasos))

pilas.avisar("Movimiento mediante comportamientos.")
pilas.ejecutar()
