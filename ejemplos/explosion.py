import pilas

imagen_explosion = pilas.imagenes.Grilla("explosion.png", 7)

def crear_explosion(sender, x, y, button, signal):
    explosion = pilas.actores.Animacion(imagen_explosion)
    explosion.x = x
    explosion.y = y
    explosion.escala = 2


pilas.eventos.click_de_mouse.connect(crear_explosion)
pilas.avisar("Pulse el boton de mouse para crear explosiones.")
pilas.ejecutar()
