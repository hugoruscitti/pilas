import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()

imagen_explosion = pilas.imagenes.cargar_grilla("explosion.png", 7)
sonido_explosion = pilas.sonidos.cargar("explosion.wav")

def crear_explosion(evento):
    explosion = pilas.actores.Animacion(imagen_explosion)
    explosion.x = evento.x
    explosion.y = evento.y
    sonido_explosion.reproducir()


pilas.escena_actual().click_de_mouse.conectar(crear_explosion)
pilas.avisar("Pulse el boton de mouse para crear explosiones.")
pilas.ejecutar()
