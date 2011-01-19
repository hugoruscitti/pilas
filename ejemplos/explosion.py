import pilas


pilas.iniciar()

imagen_explosion = pilas.imagenes.Grilla("explosion.png", 7)
sonido_explosion = pilas.sonidos.cargar("explosion.wav")

def crear_explosion(evento):
    explosion = pilas.actores.Animacion(imagen_explosion)
    explosion.x = evento.x
    explosion.y = evento.y
    sonido_explosion.reproducir()


pilas.eventos.click_de_mouse.connect(crear_explosion)
pilas.avisar("Pulse el boton de mouse para crear explosiones.")
pilas.ejecutar()
