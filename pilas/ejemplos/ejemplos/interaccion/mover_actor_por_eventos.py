import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
mono = pilas.actores.Mono()

def mover_al_mono(contexto):
    mono.x = contexto.x
    mono.y = contexto.y

# Metodo antiguo
# pilas.escena_actual().mueve_mouse.conectar(mover_al_mono)

# Nueva forma de conectar un actor a un evento.
mono.mueve_mouse(mover_al_mono)

pilas.avisar("Moviendo un actor en base a la posicion del mouse.")
pilas.ejecutar()
